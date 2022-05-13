from django.conf import settings
from django.db import models
from common.CustomLimitOffsetPaginator import genarate_rand_sting
from vendor.subapps.activity_management import models as models_activity
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.dateparse import parse_date
from common import methods as common_methods
import string
import secrets

User = settings.AUTH_USER_MODEL

STATUS = (
    ("ACTIVE", "ACTIVE"),
    ("INACTIVE", "INACTIVE"),
)

GENDER_TYPES = (
    ("MALE", "MALE"),
    ("FEMALE", "FEMALE"),
    ("OTHER", "OTHER"),
)

USER_TYPES = (
    ("VENDOR", "VENDOR"),
    ("CUSTOMER", "CUSTOMER"),
)

# Create your models here.

def genarate_user_code():
    while True:
        code = genarate_rand_sting(4)
        try:
            UserDetail.objects.get(code=code)
        except UserDetail.DoesNotExist:
            return "U"+code





FAMILY_STATUS = (
    ("ACTIVE", "ACTIVE"),
    ("SUSPENDED", "SUSPENDED"),
)


class Family(models.Model):
    superadmin = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name="family_superadmins")
    admin = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="family_admins")
    status = models.CharField(
        choices=FAMILY_STATUS, max_length=20, null=True, blank=True, default="ACTIVE")
    # Current + Future Activity Count of entire family
    upcoming_activities = models.IntegerField(default=0)
    past_activities = models.IntegerField(default=0)  # Finished Activities

    # def __str__(self):
    #     return self.superadmin.username + " - " + (self.admin.username if self.admin else "")

    # kids => related field
    def get_role_of_user(self, user):
        if (user == self.superadmin):
            return 'SUPERUSER'
        elif (user == self.admin):
            return "ADMIN"
        else:
            return None

    # def get_ongoing_upcoming_activities(self):
    #     return 0

    # def get_past_activities(self):
    #     return 0

class Kid(models.Model):
    family = models.ForeignKey(
        Family, on_delete=models.CASCADE, null=True, blank=True, related_name='kids')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='kids')
    first_name = models.CharField(
        max_length=255, blank=True, null=True, default="")
    last_name = models.CharField(
        max_length=255, blank=True, null=True, default="")
    dob = models.DateField(null=True, blank=True)
    image = models.ForeignKey('Media', on_delete=models.PROTECT,
                              related_name='kids_images', null=True, blank=True)
    avatar = models.ForeignKey('Avatar', on_delete=models.PROTECT,
                               related_name='kids_avatars', null=True, blank=True)

    def get_age(self):
        return common_methods.calculate_age(self.dob)


USER_RIGHTS = (
    ("CLASS_ENROLMENT", "CLASS_ENROLMENT"),
    ("VIEWING", "VIEWING"),
    ("SUPERUSER", "SUPERUSER"),
)


VENDOR_TYPES = (
    ('INDIVIDUAL', "INDIVIDUAL"),
    ('ORGANIZATION', "ORGANIZATION"),
)
VENDOR_STATUS = (
    ('ALL', "ALL"),
    ('ACTIVE', "ACTIVE"),
    ('SUSPENDED', "SUSPENDED"),
    ('EXPIRED', "EXPIRED"),
)


def genarate_vendor_code():
    while True:
        code = genarate_rand_sting(4)
        try:
            Vendor.objects.get(vendor_code=code)
        except Vendor.DoesNotExist:
            return code


class Vendor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.PROTECT, related_name="vendor")
    vendor_code = models.CharField(
        max_length=3, blank=True, null=True, unique=True)

    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(
        'Country', on_delete=models.PROTECT, related_name='vendors', null=True, blank=True)
    city = models.ForeignKey(
        'City', on_delete=models.PROTECT, related_name='vendors', null=True, blank=True)

    organization_type = models.CharField(
        choices=VENDOR_TYPES, max_length=20, null=True, blank=True)

    status = models.CharField(
        choices=STATUS, max_length=20, null=True, blank=True)

    vendor_status = models.CharField(
        choices=VENDOR_STATUS, max_length=20, null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='vendors_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='vendors_updated')
    # updated_at = models.DateTimeField(auto_now=True)
    # deleted_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super(Vendor, self).save(*args, **kwargs)
        self.generate_code()

    def generate_code(self):
        if self.vendor_code == "" or self.vendor_code == None:
            while(True):
                alphabet = string.ascii_uppercase + string.digits
                code = ''.join(secrets.choice(alphabet) for i in range(3))
                if(code.isnumeric()):   # Dont accept numeric strings
                    continue
                if not Vendor.objects.filter(vendor_code=code).exists():
                    self.vendor_code = code
                    self.save(update_fields=['vendor_code'])
                    break
            return code
        else:
            return False


class VendorDetails(models.Model):
    vendor = models.OneToOneField("Vendor", on_delete=models.CASCADE, related_name="vendor_details", null=True,
                                  blank=True)

    legal_name = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    entity_reg_number = models.CharField(max_length=30, blank=True, null=True)

    media = models.ManyToManyField(
        'Media', related_name='vendor_media', blank=True)
    logo = models.ForeignKey('Media', on_delete=models.PROTECT,
                             related_name='vendor_logo', null=True, blank=True)

    # profile_image = models.ImageField(blank=True, null=True)
    # profile_image = models.ForeignKey('Media', on_delete=models.SET_NULL, related_name='vendor_profile_image', null=True, blank=True)

    profile_intro = models.TextField(blank=True, null=True)

    terms = models.TextField(blank=True, null=True)

    website_visible = models.SmallIntegerField(blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)

    video_visible = models.SmallIntegerField(blank=True, null=True)
    video_introduction_url = models.URLField(
        max_length=255, blank=True, null=True)

    registered_address = models.ForeignKey('Address', on_delete=models.CASCADE,
                                           related_name='vendors_registered_address', null=True, blank=True)
    mailing_address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='vendors_mailing_address',
                                        null=True, blank=True)


class VendorSettings(models.Model):
    vendor = models.OneToOneField("Vendor", on_delete=models.CASCADE, related_name="vendor_setting", null=True,
                                  blank=True)

    max_users = models.IntegerField()
    max_locations = models.IntegerField()
    max_media = models.IntegerField()
    has_trial_class = models.BooleanField(default=False)
    has_promotions = models.BooleanField(default=False)
    has_reports = models.BooleanField(default=False)


class VendorActivitySettings(models.Model):
    vendor = models.OneToOneField("Vendor", on_delete=models.CASCADE, related_name="vendor_activity_setting", null=True,
                                  blank=True)
    activity_type = models.CharField(
        choices=models_activity.ACTIVITY_TYPES, max_length=20, null=True, blank=True)

    max_activities = models.IntegerField()


# ========================================================
#                       Signals
# ========================================================

# @receiver(pre_save, sender=User)
# def set_email_as_username(sender, instance, **kwargs):
#     print("Coming here 1", instance)
#     if (instance.email):
#         instance.username = instance.email
#
#
# @receiver(post_save, sender=User)
# def create_user_profile_if_not_exists(sender, instance, created, **kwargs):
#     print("Coming here 2", instance,created)
#     if created:
#         UserDetail.objects.create(user=instance)
#     elif not UserDetail.objects.filter(user=instance).exists():
#         UserDetail.objects.create(user=instance)
