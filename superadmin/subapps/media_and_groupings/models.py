from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime, timedelta

DECIMAL_PLACES = 2  # only applicable to methods. for model fields, change manually and migrate
STATUS = (
    ("ACTIVE", "ACTIVE"),
    ("INACTIVE", "INACTIVE"),
)

MEDIA_TYPES = (
    ("1", "Image"),
    ("2", "Video"),
    ("3", "Certificate"),
    ("4", "Document"),
)

MEDIA_USES = (
    ("CATEGORY_IMAGE", "CATEGORY_IMAGE"),
    ("CATEGORY_ICON", "CATEGORY_ICON"),
    ("SUBCATEGORY_IMAGE", "SUBCATEGORY_IMAGE"),
    ("SUBCATEGORY_ICON", "SUBCATEGORY_ICON"),
    ("BANNER_IMAGE_APP", "BANNER_IMAGE_APP"),
    ("BANNER_IMAGE_WEB", "BANNER_IMAGE_WEB"),
    ("BANNER_IMAGE_DEFAULT", "BANNER_IMAGE_DEFAULT"),
)


class AgeGroup(models.Model):
    name = models.CharField(max_length=10, blank=True, null=True)
    country=models.ForeignKey('superadmin.Country',on_delete=models.CASCADE,null=True,blank=True,related_name="agegroups")
    min_age=models.IntegerField(default=0)
    max_age=models.IntegerField(default=0)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(AgeGroup, self).save(*args, **kwargs)




class Media(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(max_length=255, blank=True, null=True)
    def __str__(self):
        return str(self.name)


AVATAR_TYPES = (
    ("BOY", "BOY"),
    ("GIRL", "GIRL"),
)


class Avatar(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(choices=AVATAR_TYPES, max_length=10, null=True, blank=True)
    media = models.ForeignKey('Media', on_delete=models.SET_NULL, related_name='avatars', null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=10, default="ACTIVE", blank=True)


# =====================================================
#               Marketing Models
# =====================================================

MARKETING_TYPE = (
    ("BANNER", "BANNER"),
    ("TRENDING", "TRENDING"),
    ("HEADER", "HEADER"),
    ("SEARCH_WORDS", "SEARCH_WORDS"),
)

MARKETING_STATUS = (
    ("ACTIVE", "ACTIVE"),
    ("SCHEDULED", "SCHEDULED"),
    ("SUSPENDED", "SUSPENDED"),
    ("EXPIRED", "EXPIRED"),
)

PLATFORM_TYPE = (
    ("WEB", "WEB"),
    ("APP", "APP"),
    # ("WEB_AND_APP", "WEB_AND_APP"),
)


class Marketing(models.Model):
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    type = models.CharField(choices=MARKETING_TYPE, max_length=20, null=True, blank=True)
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE, related_name="marketing", null=True, blank=True)
    # target_activity = models.CharField(choices=ACTIVITY_TYPES, max_length=20, null=True, blank=True)
    city = models.ForeignKey("City", on_delete=models.PROTECT, related_name="marketing", null=True, blank=True)
    platform_type = models.CharField(choices=PLATFORM_TYPE, max_length=20, null=True, blank=True)
    status = models.CharField(choices=MARKETING_STATUS, max_length=10, null=True, blank=True)
    
    total_amount_paid = models.DecimalField(decimal_places=2, max_digits=13, null=True, blank=True)
    applied_tax_rate = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True)
    transaction_id=models.CharField(max_length=30, default='')

    def get_daily_cost(self):
        if (self.total_amount_paid and self.from_date and self.to_date ):
            per_day_amount = self.total_amount_paid / (self.to_date - self.from_date + timedelta(days=1)).days
            return round(per_day_amount, DECIMAL_PLACES)
        return None 

class SearchWordDetail(models.Model):
    marketing  = models.OneToOneField("Marketing", on_delete=models.CASCADE, related_name="searchword_details", null=True, blank=True)
    # catagory = models.ForeignKey("Category", on_delete=models.PROTECT, limit_choices_to = {"subcategory": None}, related_name="banners", null=True, blank=True)
    no_of_searchwords = models.IntegerField(null=True, blank=True)
    page_visits = models.IntegerField(null=True, blank=True)

class SearchWordPricing(models.Model):
    days = models.PositiveSmallIntegerField(null=True, blank=True)
    no_of_searchwords = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=13, null=True, blank=True)



class VendorBannerDetails(models.Model):
    marketing  = models.OneToOneField("Marketing", on_delete=models.CASCADE, related_name="banner_details", null=True, blank=True)
    page_visits = models.IntegerField(null=True, blank=True)
    app_image = models.ForeignKey('Media', on_delete=models.SET_NULL, related_name='banners_app_image', null=True,
                                  blank=True)
    web_image = models.ForeignKey('Media', on_delete=models.SET_NULL, related_name='banners_web_image', null=True,
                                  blank=True)
    # vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE, related_name="banner", null=True, blank=True)
    

class AdminBanner(models.Model):
    platform_type = models.CharField(choices=PLATFORM_TYPE, max_length=20, null=True, blank=True)
    city = models.ForeignKey("City", on_delete=models.PROTECT, related_name="default_banners", null=True, blank=True)
    media = models.ForeignKey('Media', on_delete=models.SET_NULL, related_name='default_banners', null=True, blank=True)


class HeaderDetails(models.Model):
    marketing = models.OneToOneField("Marketing", on_delete=models.CASCADE, related_name="header_details", null=True,
                                     blank=True)
    page_visits = models.IntegerField()
    text = models.TextField()


class DefaultHeader(models.Model):
    date = models.DateField(blank=True, null=True)
    city = models.ForeignKey("City", on_delete=models.PROTECT, related_name="default_headers", null=True, blank=True)
    platform_type = models.CharField(choices=PLATFORM_TYPE, max_length=20, null=True, blank=True)
    text = models.TextField()


class MarketingSettings(models.Model):
    marketing_type = models.CharField(choices=MARKETING_TYPE, max_length=20, null=True, blank=True)
    platform_type = models.CharField(choices=PLATFORM_TYPE, max_length=20, null=True, blank=True)
    city = models.ForeignKey("City", on_delete=models.PROTECT, related_name="marketing_settings", null=True, blank=True)
    max_count = models.IntegerField()


class MarketingPrice(models.Model):
    city = models.ForeignKey("City", on_delete=models.PROTECT, related_name="marketing_price", null=True, blank=True)
    marketing_type = models.CharField(choices=MARKETING_TYPE, max_length=20, null=True, blank=True)
    platform_type = models.CharField(choices=PLATFORM_TYPE, max_length=20, null=True, blank=True)
    # catagory = models.ForeignKey("Category", on_delete=models.CASCADE, limit_choices_to = {"subcategory": None}, related_name="marketing_price", null=True, blank=True)
    category = models.CharField(max_length=100,null=True, blank=True)
    days = models.PositiveSmallIntegerField(null=True, blank=True) # Days value None will be used to indicated Subsequent Days entry
    price = models.DecimalField(max_digits=10 ,decimal_places=2,null=True)

class MarketingGenericPrice(models.Model):
    marketing = models.ForeignKey("Marketing", on_delete=models.CASCADE, related_name="marketing_generic_price",
                                  null=True, blank=True)
    platform_type = models.CharField(choices=PLATFORM_TYPE, max_length=20, null=True, blank=True)
    city = models.ForeignKey("City", on_delete=models.PROTECT, related_name="marketing_generic_price", null=True,
                             blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class MarketingWordDetail(models.Model):
    marketing = models.ForeignKey("Marketing", on_delete=models.CASCADE, related_name="marketing_word_detais",
                                  null=True, blank=True)
    word = models.CharField(max_length=100, null=True, blank=True)
    page_visits = models.IntegerField()
