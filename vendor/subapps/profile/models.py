from django.db import models
from superadmin.subapps.countries_and_cities.models import City, Area, Region
from django.contrib.auth import get_user_model

User = get_user_model()

VENDOR_STATUS = (
    ('ACTIVE', "ACTIVE"),
    ('SUSPENDED', "SUSPENDED"),
    ('EXPIRED', "EXPIRED"),
)
class VendorProfile(models.Model):
    

    ORGANIZATION_TYPES=(
        ('INDIVIDUAL','INDIVIDUAL'),
        ('ENTITY','ENTITY'),
    )
    vendor=models.OneToOneField(User,on_delete=models.PROTECT,related_name="vendor_profile")
    organization_type=models.CharField(max_length=25,choices=ORGANIZATION_TYPES,null=True,blank=True)
    name=models.CharField(max_length=255,null=True,blank=True)
    reg_address=models.TextField(null=True,blank=True)
    reg_city=models.CharField(max_length=25)
    reg_zip_code=models.CharField(max_length=10)
    mailing_address=models.TextField(null=True,blank=True)
    mailing_city=models.CharField(max_length=25,null=True,blank=True)
    mailing_zip_code=models.CharField(max_length=10,null=True,blank=True)
    reg_number=models.CharField(max_length=255,null=True,blank=True)
    preferred_name=models.CharField(max_length=40)
    profile_intro=models.TextField(max_length=1600)
    terms_and_conditions=models.TextField(max_length=10000,null=True,blank=True)
    logo=models.ImageField(upload_to='vendor/logos',null=True,blank=True)
    is_website=models.BooleanField(default=False)
    website_url=models.CharField(max_length=255,null=True,blank=True)
    is_instagram=models.BooleanField(default=False)
    instagram_url=models.CharField(max_length=255,null=True,blank=True)
    is_twitter=models.BooleanField(default=False)
    twitter_url=models.CharField(max_length=255,null=True,blank=True)
    is_facebook=models.BooleanField(default=False)
    facebook_url=models.CharField(max_length=255,null=True,blank=True)

    vendor_status=models.CharField(max_length=20,default='ACTIVE',choices=VENDOR_STATUS)

    def __str__(self):
        return self.name

class VendorBanner(models.Model):
    vendor=models.ForeignKey(VendorProfile,on_delete=models.CASCADE,related_name="banners")
    banner=models.ImageField(upload_to="vendor/banners")


class VendorLocation(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.PROTECT, related_name="locations", null=True,blank=True)
    shortname = models.CharField(max_length=10, null=True, blank=True )
    address = models.TextField(max_length=100, null=True, blank=True)
    status = models.TextField(max_length=10,null=True, blank=True)
    city = models.ForeignKey(City, on_delete= models.CASCADE, related_name='vendor_city',null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='vendor_region', null=True, blank=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='vendor_area',null=True, blank=True)
    