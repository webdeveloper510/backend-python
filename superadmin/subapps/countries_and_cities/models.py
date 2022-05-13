from django.core.exceptions import ValidationError
from django.db import models
from superadmin.subapps.vendor_and_user_management import models as models_users
# Create your models here.

STATUS = (
    ("ACTIVE", "ACTIVE"),
    ("INACTIVE", "INACTIVE"),
)


class Country(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, unique=True)
    abbr = models.CharField(max_length=2, blank=True, null=True)
    status = models.CharField(choices=STATUS, max_length=10, null=True, blank=True, default="INACTIVE")
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name', )

    def save(self, *args, **kwargs):
        if self.name == None:
            raise ValidationError('Name field is required')
        return super(Country, self).save(*args, **kwargs)


class Currency(models.Model):
    country = models.OneToOneField(
        'Country', on_delete=models.CASCADE, related_name='currency', null=True, blank=True)
    
    display_character = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey("Country", on_delete=models.PROTECT, related_name="cities", null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=10, null=True, blank=True, default="ACTIVE")


    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name == None or len(self.name) <3:
            raise ValidationError('Cities name must be three charecter.')

        if self.country == None:
            raise ValidationError("Country field is required")
        return super(City, self).save(*args, **kwargs)



class Region(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    city = models.ForeignKey("City", on_delete=models.PROTECT, related_name="regions", null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=10, null=True, blank=True, default="ACTIVE")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if (self.name == None):
            raise ValidationError("Name is required")
        if (len(self.name) <3):
            raise ValidationError("Name must be three charecters")
        
        return super(Region, self).save(*args, **kwargs)

class Area(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    region = models.ForeignKey("Region", on_delete=models.PROTECT, related_name="areas", null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=10, null=True, blank=True, default="ACTIVE")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if (self.name == None):
            raise ValidationError("Name is required")
        if (len(self.name) <3):
            raise ValidationError("Name must be three charecters")
        
        return super(Area, self).save(*args, **kwargs)

class Address(models.Model):
    address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    phone_office = models.CharField(max_length=20, blank=True, null=True)
    phone_mobile = models.CharField(max_length=20, blank=True, null=True)
    zipcode = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return self.address_line_1

