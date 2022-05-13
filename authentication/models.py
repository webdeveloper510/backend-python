from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from numpy import true_divide
from rest_framework_simplejwt.tokens import RefreshToken
from superadmin.subapps.countries_and_cities.models import City, Area, Region, Country
from common.CustomLimitOffsetPaginator import genarate_rand_sting
from django.conf import settings

USER_TYPES = (
    ("VENDOR", "VENDOR"),
    ("CUSTOMER", "CUSTOMER"),
)

GENDER_TYPES = (
    ("MALE", "MALE"),
    ("FEMALE", "FEMALE"),
    ("OTHER", "OTHER"),
)

def genarate_user_code():
    while True:
        code = genarate_rand_sting(5)
        try:
            UserProfile.objects.get(user__username=code)
        except UserProfile.DoesNotExist:
            return "U"+code


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}

class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))
    date_joined = models.DateField(auto_now_add=True,null=True,blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="userdetails")
    code=models.CharField(max_length=15,null=True,blank=True)
    firstname = models.CharField(max_length=30,blank=True, null=True)
    lastname = models.CharField(max_length=30, blank=True, null=True)
    dob=models.DateField(null=True,blank=True)
    role = models.CharField(
        choices=USER_TYPES, max_length=20, blank=True, null=True)  # type
    country = models.ForeignKey(
        Country, on_delete=models.PROTECT, related_name='country', null=True, blank=True)
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name='city', null=True, blank=True)

    def __str__(self):
        return str(self.user)



class userdetail(models.Model):
    code=models.CharField(max_length=15,null=True,blank=True)
    firstname = models.CharField(max_length=30,blank=True, null=True)
    lastname = models.CharField(max_length=30, blank=True, null=True)
    dob=models.DateField(null=True,blank=True)
    active=models.CharField(max_length=20,null=True,blank=True)





class activity(models.Model):
    vendor_name=models.CharField(max_length=200,null=True)
    vendor_code=models.CharField(max_length=200,null=True)
    activity_title=models.CharField(max_length=200,null=True)
    activity_code=models.CharField(max_length=200,null=True)
    country=models.CharField(max_length=200,null=True)
    activity_type=models.CharField(max_length=200,null=True)
    available_future_classes=models.IntegerField(null=True)
    available_future_sessions=models.IntegerField(null=True)
    session_of_classes=models.IntegerField(null=True)
    status=models.BooleanField(default=True)
    created=models.DateTimeField(null=True,blank=True,auto_now_add=True)
    start_date=models.DateTimeField(null=True,blank=True,auto_now_add=True)
    end_date=models.DateTimeField(null=True,blank=True,auto_now_add=True)


