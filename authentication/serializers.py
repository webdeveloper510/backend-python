from pyexpat import model
from numpy import vander
from rest_framework import serializers
from .models import User, userdetail,activity,Vendor
from rest_framework import generics
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        return attrs

    def create(self, validated_data):
        instance = User.objects.create_user(**validated_data)
        return instance


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

        return super().validate(attrs)


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    email = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'email']

    def validate(self, attrs):
        # try:
            password = attrs.get('password')
            token = attrs.get('token')
            email = attrs.get('email')

            # id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(email=email)
            print('user is ', user,token)
            # if not PasswordResetTokenGenerator().check_token(user, token):
            #     raise AuthenticationFailed('The reset link is invalid', 401)
            user.set_password(password)
            user.save()

            return (user)
        # except Exception as e:
        #     raise AuthenticationFailed('The reset link is invalid', 401)
       # return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')




class registerSerializer(serializers.ModelSerializer):
        model = userdetail
        fields = ['email','code','firstname','dob','active']


class activitySerializer(serializers.ModelSerializer):
 
 
 class Meta:
     model = activity
     fields = '__all__'

class statuscheck(serializers.ModelSerializer):
    vendor_name=serializers.CharField()
    
    class Meta:
        model=activity
        fields=['vendor_name']     

class unactiveSerializer(serializers.ModelSerializer):
 start_date = serializers.DateTimeField()
 end_date = serializers.DateTimeField()

 class Meta:
     model = activity
     fields =['start_date','end_date']   



# class statuscheckSerializer(serializers.ModelSerializer):
#  vendor_name=serializers.CharField()

#  class Meta:
#      model=activity
#      fields=['vendor_name']



# class searchSerializer(serializers.ModelSerializer):
 
 
#  class Meta:
#      model = activity
#      fields = '__all__'

        

class activityVendorSerializer(serializers.ModelSerializer):
 
 
 class Meta:
     model = Vendor
     fields = '__all__'

