from superadmin.subapps.settings.models import UserAdminInvitation
from rest_framework import serializers
from django.contrib.auth import get_user_model

#from .models import UserDetail

User = get_user_model()

from . import models
from superadmin.subapps.countries_and_cities import models as models_country

from superadmin.subapps.countries_and_cities import serializers as serializers_country
from superadmin.subapps.media_and_groupings import models as models_media
from superadmin import custom_serializers_fields as csf

from superadmin.subapps.media_and_groupings import methods

from django.db import transaction
from django.db import IntegrityError
# from datetime import datetime, timedelta
from django.utils import timezone
# =================================================
#                User Serializers
# =================================================

USER_TYPES = (
    ("VENDOR", "VENDOR"),
    ("CUSTOMER", "CUSTOMER"),
)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'is_active')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print("*******************************", validated_data)
        instance = super(UserSerializer, self).create(validated_data)
        if ('password' in validated_data):
            password = validated_data.pop('password')
        instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        if ('password' in validated_data):
            password = validated_data.pop('password')
            instance.set_password(password)
        instance.save()
        super(UserSerializer, self).update(instance, validated_data)
        return instance


class UserDetailSerializer(serializers.ModelSerializer):
    email= serializers.CharField()
    city = serializers.CharField()
    country = serializers.CharField()

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        print("**************************", validated_data)
        name = validated_data.pop('email')
        city = validated_data.pop("city")
        country = validated_data.pop("country")
        print("value is",name)
        instance = UserDetail.objects.get(user=name)
        c = models_country.City.objects.get(name=city)
        country_obj = models_country.Country.objects.get(name=country)
        instance.city = c
        instance.country = country_obj
        instance.status = "ACTIVE"
        instance.role = "CONSUMER"

        instance.save()
        return instance


class UserRegistrationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False)
    password = serializers.CharField(write_only=True)
    city = serializers.CharField(source="userdetails.city")
    country = serializers.CharField(source="userdetails.country")
    email = serializers.CharField()

    class Meta:
        model = User
        fields = ('id', 'password', 'first_name',
                  'last_name', 'email', 'city', 'country')
        extra_kwargs = {'password': {'write_only': True}}
        write_only_fields = ('password',)

    def create(self, validated_data):
        print("********************************",validated_data)
        if ('id' in validated_data):
            id = validated_data.pop('id')  # Drop ID at object creation
        userdetails = validated_data.pop("userdetails")
        print(userdetails)
        city = userdetails.pop("city")
        country = userdetails.pop("country")


        validated_data['username'] = validated_data['email']
        if ('password' in validated_data):
            password = validated_data.pop('password')

        with transaction.atomic():
            # instance.save(update_fields='password')
            try:
                instance = super(UserRegistrationSerializer,
                                 self).create(validated_data)
                instance.set_password(password)
                instance.save()
                pass
            except IntegrityError:
                raise serializers.ValidationError(
                    {"error": "user with given email already exists"})
            except:
                raise serializers.ValidationError(
                    {"error": "unexpected error occured at server"})
            try:
                country_obj = models_country.Country.objects.get(name=country)
            except:
                raise serializers.ValidationError(
                    {"country": "country does not exists"})
            try:
                c = models_country.City.objects.get(
                    name=city, country__name=country)
            except:
                raise serializers.ValidationError(
                    {"city": "city does not exists"})

            instance.userdetails.city = c
            instance.userdetails.country = country_obj
            instance.userdetails.status = "ACTIVE"
            instance.userdetails.role = "CONSUMER"
            instance.userdetails.save(
                update_fields=['city', 'country', 'status', 'role'])

        return instance

    def update(self, instance, validated_data):
        if ('id' in validated_data):
            id = validated_data.pop('id')  # Drop ID at object creation

        if ('password' in validated_data):
            password = validated_data.pop('password')
            instance.set_password(password)

        if ('email' in validated_data):
            if (validated_data['email'] != instance.username):
                validated_data['username'] = validated_data['email']
        # if "userdetails" in validated_data:
        try:
            userdetails = validated_data.pop("userdetails")
            city = userdetails.pop("city")
            country = userdetails.pop("country")
        except:
            city = None
            country = None

        with transaction.atomic():
            try:
                instance = super(UserRegistrationSerializer, self).update(
                    instance, validated_data)
            except IntegrityError:
                raise serializers.ValidationError(
                    {"error": "user with given email already exists"})
            except Exception as e:
                print(e)
                raise serializers.ValidationError(
                    {"error": "unexpected error occured at server"})
            if country:
                try:
                    country_obj = models_country.Country.objects.get(
                        name=country)
                except:
                    raise serializers.ValidationError(
                        {"country": "country does not exists"})
                instance.userdetails.country = country_obj
            if city:
                try:
                    c = models_country.City.objects.get(
                        name=city, country__name=country)
                except:
                    raise serializers.ValidationError(
                        {"city": "city does not exists"})
                instance.userdetails.city = c
            instance.userdetails.save(update_fields=['city', 'country'])
            family = models.Family.objects.create(
                    superadmin=instance, status="ACTIVE")
            instance.userdetails.family = family
            instance.userdetails.save(update_fields=["family"])
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source="userdetails.city")
    country = serializers.CharField(source="userdetails.country")
    dob = serializers.CharField(source="userdetails.dob")
    email = serializers.CharField()
    role = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    # profile_image = csf.ReadWriteSerializerMethodField(
    #     allow_null=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'password', 'first_name', 'last_name', 'email',
                  'city', 'country', 'dob', 'age', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def get_role(self, obj):
        return obj.userdetails.family.get_role_of_user(obj) if obj.userdetails.family else None

    def get_age(self, obj):
        return obj.userdetails.get_age() if obj.userdetails else None

    def update(self, instance, validated_data):
        country, city, dob = None, None, None
        if ('password' in validated_data):
            password = validated_data.pop('password')
            instance.set_password(password)

        if ('email' in validated_data):
            if (validated_data['email'] != instance.username):
                validated_data['username'] = validated_data['email']

        userdetails = validated_data.get("userdetails")
        if userdetails:
            validated_data.pop("userdetails")

            country = userdetails.get("country")
            if country:
                city = userdetails.get("city")
            dob = userdetails.get("dob")
        # profile_image = userdetails.pop("profile_image")

        with transaction.atomic():
            try:
                instance = super(UserProfileSerializer, self).update(
                    instance, validated_data)
            except IntegrityError:
                raise serializers.ValidationError(
                    {"error": "user with given email already exists"})
            except:
                raise serializers.ValidationError(
                    {"error": "unexpected error occured at server"})
            if country:
                try:
                    country_obj = models_country.Country.objects.get(
                        name=country)

                except:
                    raise serializers.ValidationError(
                        {"country": "country does not exists"})

                instance.userdetails.country = country_obj
            if city:
                try:
                    c = models_country.City.objects.get(
                        name=city, country__name=country)
                except:
                    raise serializers.ValidationError(
                        {"city": "city does not exists"})

                instance.userdetails.city = c

            if dob:
                instance.userdetails.dob = dob
            instance.userdetails.save()

            # if ('profile_image' in validated_data):
            #     profile_image = validated_data.pop('profile_image', None)
            #     if (profile_image == None):
            #         profile_image = {"file": None}
            #     # methods.update_media_object(instance.userdetails, 'profile_image', dict=profile_image_dict)
            #     methods.update_media_field(
            #         instance.userdetails, 'profile_image', profile_image, name=None, status="ACTIVE", type=None)
        instance.save()
        return instance


class UpdateUserProfileSerializer(UserProfileSerializer):
    email = serializers.CharField(required=False)

# =================================================
#                Family Serializers
# =================================================


class KidSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()

    class Meta:
        model = models.Kid
        # fields = '__all__'
        fields = ('id', 'first_name', 'last_name', 'code',
                  'dob', 'age',  'avatar', 'image')
        extra_kwargs = {
            'avatar': {'write_only': True, 'required': False}
        }

    def get_image(self, obj):
        return obj.image.file.url if obj.image and obj.image.file else None

    def get_age(self, obj):
        return obj.get_age() if obj.dob != None and obj.dob != "" else None

    def get_code(self, obj):
        try:
            return obj.user.userdetails.code
        except:
            return None

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        avatar = validated_data.get('avatar', None)

        with transaction.atomic():
            instance = super(KidSerializer, self).create(validated_data)
            if (image):
                file = image.pop("file", None)
                methods.update_media_field(
                    instance, "image", file, name="KID_IMAGE", status="ACTIVE", type=None)
            elif (avatar):
                try:
                    avatar_file_url = avatar.media
                except Exception as e:
                    raise serializers.ValidationError(
                        {'avatar': "Avatar not found"})

                instance.image = avatar_file_url
                instance.avatar = avatar
                print(avatar.media)
                instance.save()

        return instance

    def update(self, instance, validated_data):
        if 'avatar' in validated_data:
            avatar = validated_data.get('avatar', None)

            try:
                avatar_file_url = avatar.media
            except Exception as e:
                raise serializers.ValidationError(
                    {'avatar': "Avatar file not found."})

            instance.image = avatar_file_url
            instance.avatar = avatar
            instance.save()

        if('image' in validated_data):
            image = validated_data.pop('image', None)
            if (image and type(image) is dict):
                file = image.pop("file", None)
                methods.update_media_field(
                    instance, "image", file, name="KID_IMAGE", status="ACTIVE", type=None)
                instance.avatar = None

            else:
                raise serializers.ValidationError(
                    {"error": 'The image field expects media object with fields file and name.'})

        instance = super(KidSerializer, self).update(instance, validated_data)
        return instance


class FamilyUserSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source="userdetails.country.name")
    first_name = serializers.CharField(source="userdetails.firstname")
    last_name = serializers.CharField(source="userdetails.lastname")
    email = serializers.CharField()
    profile_image = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()

    def get_profile_image(self, obj):
        return None
        #return obj.userdetails.profile_image.file.url if obj.userdetails and obj.userdetails.profile_image and obj.userdetails.profile_image.file else ""

    def get_code(self, obj):
        try:
            return obj.userdetails.code
        except:
            return None

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'code', 'country', 'profile_image')


class FamilySerializer(serializers.ModelSerializer):
    superadmin = FamilyUserSerializer()
    admin = FamilyUserSerializer()
    kids = KidSerializer(many=True)
    # invitations = serializers.SerializerMethodField()

    class Meta:
        model = models.Family
        fields = ('id','superadmin', 'admin', 'kids', 'upcoming_activities',
                  'past_activities', 'status')
        read_only_fields = ('upcoming_activities', 'past_activities')

    # def get_invitations(self, obj):
    #     return 'SENT' if obj.superadmin.invitations_sent.filter(status='ACTIVE').exists() else None

    def update(self, instance, validated_data):
        if ('superadmin' in validated_data):
            validated_data.pop('superadmin')

        if ('admin' in validated_data):
            validated_data.pop('admin')

        if ('kids' in validated_data):
            validated_data.pop('kids')

        instance = super(FamilySerializer, self).update(
            instance, validated_data)
        return instance


# =================================================
#                Vendor Serializers
# =================================================

class VendorDetailsSerializer(serializers.ModelSerializer):
    media = csf.ReadWriteSerializerMethodField(allow_null=True, required=False)
    logo = csf.ReadWriteSerializerMethodField(allow_null=True, required=False)

    registered_address = serializers_country.AddressSerializer()
    mailing_address = serializers_country.AddressSerializer()

    class Meta:
        model = models.VendorDetails
        fields = '__all__'

    def get_logo(self, obj):
        return obj.logo.file.url if obj.logo and obj.logo.file else None

    def get_media(self, obj):
        return obj.media.all() if obj.media else None

    def create(self, validated_data):
        registered_address = validated_data.pop('registered_address')
        mailing_address = validated_data.pop('mailing_address')
        media = validated_data.pop('media')
        logo = validated_data.pop('logo', None)

        with transaction.atomic():
            registered_address = models_country.Address.objects.create(
                **registered_address)
            mailing_address = models_country.Address.objects.create(
                **mailing_address)
            if (logo):
                logo = models_media.Media.objects.create(**logo)

            instance = models.VendorDetails.objects.create(**validated_data,
                                                           registered_address=registered_address,
                                                           mailing_address=mailing_address, logo=logo)

            for obj in media:
                file = obj.get('file')
                name = obj.get('name', '')
                if (file != None):
                    obj = {"file": file, "name": name}
                    try:
                        media_obj = models_media.Media.objects.create(
                            **obj, status="ACTIVE")
                    except:
                        raise serializers.ValidationError(
                            {"media": 'invalid media file supplied'})

                    instance.media.add(media_obj)

        return instance

    def update(self, instance, validated_data):
        if ('registered_address' in validated_data):
            registered_address = validated_data.pop('registered_address')
            serializer = serializers_country.AddressSerializer(
                instance.registered_address, data=registered_address)
            if (serializer.is_valid()):
                serializer.save()
            else:
                self.errors.update(serializer.errors)

        if ('mailing_address' in validated_data):
            mailing_address = validated_data.pop('mailing_address')
            serializer = serializers_country.AddressSerializer(
                instance.mailing_address, data=mailing_address)
            if (serializer.is_valid()):
                serializer.save()
            else:
                self.errors.update(serializer.errors)

        if ('media' in validated_data):
            media = validated_data.pop('media')

            for obj in media:
                if ('id' in obj):  # Update or delete
                    file = obj.get('file')
                    if (file == None):
                        try:
                            m = models_media.Media.objects.get(
                                id=obj.get('id'), status="ACTIVE")
                        except:
                            raise serializers.ValidationError(
                                {"media": 'media object with id ' + str(obj.get('id')) + " does not exists"})

                        if (
                                m not in instance.media.all()):  # Media object exists but not associated with given vendor media. This is to prevent rendom media object updates from this endpoint
                            raise serializers.ValidationError(
                                {"media": 'media object with id ' + str(obj.get('id')) + " does not exists"})

                        m.status = "INACTIVE"
                        m.save(update_fields=['status'])
                        instance.media.remove(m)
                else:  # Create
                    file = obj.get('file')
                    if (file != None):
                        obj = {"file": file}
                        media_obj = models_media.Media.objects.create(
                            **obj, status="ACTIVE")
                        instance.media.add(media_obj)

        if ('logo' in validated_data):
            logo = validated_data.pop('logo', {"file": None})
            if (logo == None):
                logo = {"file": None}
            methods.update_media_object(instance, 'logo', dict=logo)

        instance.save()  # comment it and test
        super(VendorDetailsSerializer, self).update(instance, validated_data)
        return instance


class VendorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    password = serializers.CharField(write_only=True, source="user.password")
    vendor_code = serializers.CharField(read_only=True)
    country = serializers.CharField()
    city = serializers.CharField()
    legal_name = serializers.CharField(source="vendor_details.legal_name")
    code = serializers.CharField(source="vendor_details.code")
    entity_reg_number = serializers.CharField(
        source="vendor_details.entity_reg_number")
    # media = serializers_categories.MediaSerializer(
    #     source="vendor_details.media", many=True)
    #
    # logo = serializers_categories.MediaSerializer(
    #     source="vendor_details.logo", many=False, allow_null=True, required=False)

    profile_intro = serializers.CharField(
        source="vendor_details.profile_intro")
    terms = serializers.CharField(source="vendor_details.terms")
    website = serializers.CharField(source="vendor_details.website")
    video_introduction_url = serializers.CharField(source="vendor_details.video_introduction_url", allow_blank=True,
                                                   allow_null=True)
    registered_address = serializers_country.AddressSerializer(
        source="vendor_details.registered_address")
    mailing_address = serializers_country.AddressSerializer(
        source="vendor_details.mailing_address")
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = models.Vendor
        fields = (
            'id', 'username', 'password', 'name', 'vendor_code', 'email', 'country', 'city', 'vendor_status', 'organization_type',
            'legal_name', 'code', 'entity_reg_number', 'profile_intro', 'terms', 'website',
            'video_introduction_url', 'registered_address', 'mailing_address', 'created_at')

    def get_created_at(self, obj):
        return obj.created_at.isoformat()

    def get_logo(self, obj):
        return obj.vendor_details.logo.file.url if obj.vendor_details.logo.file else None

    def create(self, validated_data):
        user = validated_data.pop('user')
        country = validated_data.pop('country')
        city = validated_data.pop('city')
        vendor_details = validated_data.pop('vendor_details')

        with transaction.atomic():
            c = models_country.Country.objects.get(name=country)
            try:
                city_obj = models_country.City.objects.get(name=city)
            except:
                raise serializers.ValidationError(
                    {"city": "invalid city name"})

            serializer = UserSerializer(data=user, partial=True)
            if (serializer.is_valid()):
                user_obj = serializer.save()
            else:
                self.errors.update(serializer.errors)
                raise serializers.ValidationError(serializer.errors)

            vendor = models.Vendor.objects.create(
                **validated_data, user=user_obj, country=c, city=city_obj)

            serializer = VendorDetailsSerializer(data=vendor_details)
            if (serializer.is_valid()):
                vd = serializer.save()
                vd.vendor = vendor
                vd.save(update_fields=['vendor'])
            else:
                vendor.delete()
                self.errors.update(serializer.errors)
                raise serializers.ValidationError(serializer.errors)

        return vendor

    def update(self, instance, validated_data):
        if ('user' in validated_data):
            userdata = validated_data.pop('user')
            serializer = UserSerializer(
                instance.user, data=userdata, partial=True)
            if (serializer.is_valid()):
                serializer.save()
            else:
                self.errors.update(serializer.errors)
                raise serializers.ValidationError(serializer.errors)

        if ('country' in validated_data):
            country = validated_data.pop('country')
            try:
                c = models_country.Country.objects.get(name=country)
                instance.country = c
            except:
                raise serializers.ValidationError(
                    {"country": "invalid country name"})

        if ('city' in validated_data):
            city = validated_data.pop('city')
            try:
                c = models_country.City.objects.get(name=city)
                instance.city = c
            except:
                raise serializers.ValidationError(
                    {"city": "invalid city name"})
        if ('vendor_details' in validated_data):
            serializer = VendorDetailsSerializer(instance.vendor_details, data=validated_data.pop('vendor_details'),
                                                 partial=True)

            if (serializer.is_valid()):
                vd = serializer.save()
            else:
                self.errors.update(serializer.errors)
                raise serializers.ValidationError(serializer.errors)

        instance.save(update_fields=['country'])
        super(VendorSerializer, self).update(instance, validated_data)
        return instance
