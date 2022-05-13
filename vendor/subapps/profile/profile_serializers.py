from rest_framework import serializers
from django.core import exceptions
from django.contrib.auth import password_validation
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from .models import  VendorBanner, VendorProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    firstname=serializers.CharField(source='userdetails.firstname')
    lastname=serializers.CharField(source='userdetails.lastname')
    code=serializers.CharField(source='userdetails.code')
    country=serializers.CharField(source='userdetails.country.name')

    class Meta:
        model = User
        fields = ('id','firstname','lastname','code','date_joined',"country",'email')

class ChangePasswordSerializer(serializers.Serializer):
    old_password=serializers.CharField()
    new_password=serializers.CharField()
    confirm_password=serializers.CharField()

    def create(self,validated_data):
        old_password=validated_data.get('old_password')
        new_password=validated_data.get('new_password')
        confirm_password=validated_data.get('confirm_password')

        user = self.context['request'].user

        try:
            # validate the password and catch the exception
            password_validation.validate_password(
                password=new_password, user=User)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            # errors['new_password'] = list(e.messages)
            raise serializers.ValidationError(
                {'new_password': [e.messages]})

        

        if confirm_password!=new_password:
            raise serializers.ValidationError({"error":"Passwords don't match."})
        
        if user.check_password(old_password) == False:
            raise serializers.ValidationError({"error":"Invalid Old Password."})

        user.set_password(new_password)

        user.save()
        return user

class ChangeNameSerializer(serializers.Serializer):
    name=serializers.CharField()

    def create(self, validated_data):
        user = self.context['request'].user
        name=validated_data.get('name')
        user.username = name
        user.save()
        
        return user

class VendorBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorBanner
        fields = '__all__'
        extra_kwargs={"vendor":{"required":False}}

class VendorProfileSerializer(serializers.ModelSerializer):
    vendor=UserSerializer(read_only=True)

    def create(self,validated_data):
        try:
            instance = self.Meta.model(vendor=self.context["request"].user,**validated_data)
            instance.save()
        except IntegrityError:
            raise serializers.ValidationError({"error":"Vendor Profile Already Created user PUT request to Update it."})
        return instance

    class Meta:
        model=VendorProfile
        fields='__all__'
        extra_kwargs={"vendor":{"required":False}}