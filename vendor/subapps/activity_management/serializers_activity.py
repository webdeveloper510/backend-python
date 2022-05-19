from multiprocessing.dummy import active_children
import random
import string
import base64
import random
import os
from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import get_user_model
from superadmin.subapps.vendor_and_user_management.models import Vendor
User=get_user_model()

from . import models, methods

from superadmin.subapps.media_and_groupings.models import AgeGroup as agegroupmodel
from superadmin import custom_serializers_fields as csf

from .serializers_attributes import AttributeSerializer,SubAttributeSerializer


class MediaListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(status="ACTIVE")
        return super(MediaListSerializer, self).to_representation(data)

class MediaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    file = csf.CustomBase64FileField(allow_null=True)
    class Meta:
        model = models.Media
        # fields = '__all__'
        fields = ('id','name', 'file')
        # fields = ('file')
        list_serializer_class = MediaListSerializer
    def create(self, validated_data):
        m = super(MediaSerializer, self).create(validated_data)
        return m

class MediaDetailSerializer(serializers.ModelSerializer):
    file = csf.CustomBase64FileField()
    class Meta:
        model = models.Media
        fields = '__all__'
        # fields = ('name', 'file', 'type', 'status')
        # fields = ('file')


class BannerSerializers (serializers.ModelSerializer):

    class Meta:
        model = models.Banner
        fields = '__all__'

    def create(self, validated_data):
        print('validates data is', validated_data)
        m = super(BannerSerializers, self).create(validated_data)
        return m


class UserSerializer(serializers.ModelSerializer):
    firstname=serializers.CharField(source='userdetails.firstname')
    lastname=serializers.CharField(source='userdetails.lastname')
    class Meta:
        model=User
        fields=['id','firstname','lastname','email']


class activityStatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vendor
        fields = '__all__'

class activitytypeSerializer(serializers.ModelSerializer):
    gett=serializers.CharField(source='updated_by.code')
    print(gett)
    class Meta:
        model = Vendor
        fields = '__all__'


class ActivitySerializers (serializers.ModelSerializer):
    agegroups = serializers.ListField(child=serializers.CharField(),required=False)
    subattributes = serializers.ListField(child=serializers.IntegerField(),required=False)
    agegroupsList=serializers.SerializerMethodField()
    attributesList=serializers.SerializerMethodField()
    updated_by=UserSerializer()

    def get_agegroupsList(self,obj):
        res = models.ActivityAgeGroups.objects.filter(activity=obj).values('agegroup__name')
        return res
    
    def get_attributesList(self,obj):
        results = obj.attributesList.all()
        serializedResults = []
        for result in results:
            serializer = SubAttributeSerializer(result.subAttribute)
            serializedResults.append(serializer.data)
        return serializedResults

    class Meta:
        model = models.Activity
        fields = '__all__'
        extra_fields = ['agegroupsList','attributesList']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(ActivitySerializers, self).get_field_names(declared_fields, info)
        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

    def savefile(self, file):
        b = file.split(';base64,')
        a = b[1]
        c = b[0].split('/')
        subDir = 'coverimage/'
        file_path = str(settings.MEDIA_ROOT) + '/' + subDir
        if not os.path.isdir(file_path):
            os.makedirs(file_path, mode=0o777)
        randStr = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=6)) + '.' + c[1]
        file_path = file_path + randStr
        d = base64.b64decode(a)
        decodeit = open(file_path, 'wb')
        decodeit.write(d)
        decodeit.close()
        media_url = settings.MEDIA_URL + subDir + randStr
        return media_url

    def savebanners(self, bannerfile):
        b = bannerfile.split(';base64,')
        a = b[1]
        c = b[0].split('/')
        subDir = 'banners/'
        file_path = str(settings.MEDIA_ROOT) + '/' + subDir
        if not os.path.isdir(file_path):
            os.makedirs(file_path, mode=0o777)
        randStr = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=6)) + '.' + c[1]
        file_path = file_path + randStr
        d = base64.b64decode(a)
        decodeit = open(file_path, 'wb')
        decodeit.write(d)
        decodeit.close()
        media_url = settings.MEDIA_URL + subDir + randStr
        return media_url

    def create(self, validated_data):
        agegroups = validated_data.pop('agegroups')
        subattributes = validated_data.pop('subattributes')
        banner = validated_data.pop('banner',None)

        codetoadd = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        instance = models.Activity.objects.create(**validated_data)

        if agegroups:
            for agegroup in agegroups:
                agegroup = agegroupmodel.objects.get(name=agegroup)
                models.ActivityAgeGroups.objects.create(activity=instance,agegroup=agegroup)

        if subattributes:
            for sa in subattributes:
                subattribute = models.SubAttribute.objects.get(id=sa)
                models.ActivitySubAttributes.objects.create(activity=instance,subAttribute=subattribute)

        if banner:
            for singlebanner in banner:
                filepath = self.savebanners(singlebanner['filepath'])
                serializer = BannerSerializers(data={'filepath':filepath}, partial=True)
                if serializer.is_valid():
                    obj = serializer.save(banner=instance)
                    obj.save()
                else:
                    raise serializers.ValidationError({"error": serializer.errors})
        instance.code = codetoadd
        instance.save()
        return instance

    def update(self, instance, validated_data):
        # if 'coverimage' in validated_data:
        #     coverimage = validated_data.pop('coverimage')
        #     if coverimage:
        #         filepath = self.savefile(coverimage)
        #         validated_data['coverimage'] = filepath
        agegroups = validated_data.pop('agegroups')
        subattributes = validated_data.pop('subattributes')

        validated_data.pop("noofsessions",None)
        validated_data.pop("tierpricing",None)
        validated_data.pop("tierPricingcheckbox1",None)
        validated_data.pop("tierdescription1",None)
        validated_data.pop("tierPricingcheckbox2",None)
        validated_data.pop("tierdescription2",None)
        validated_data.pop("tierPricingcheckbox3",None)
        validated_data.pop("tierdescription3",None)


        if agegroups:
            models.ActivityAgeGroups.objects.filter(activity=instance).delete()
            for agegroup in agegroups:
                agegroup = agegroupmodel.objects.get(name=agegroup)
                models.ActivityAgeGroups.objects.create(activity=instance,agegroup=agegroup)

        if subattributes:
            models.ActivitySubAttributes.objects.filter(activity=instance).delete()
            for sa in subattributes:
                subattribute = models.SubAttribute.objects.get(id=sa)
                models.ActivitySubAttributes.objects.create(activity=instance,subAttribute=subattribute)


        super(ActivitySerializers, self).update(instance, validated_data)
        instance.save()
        return instance

    def get_coverimage(self, obj):
        return obj.coverimage.file.url if obj.coverimage and obj.coverimage.file else None

    def get_media(self, obj):
        return obj.media.all() if obj.media else None

