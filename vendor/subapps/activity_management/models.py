from email.policy import default
from pyexpat import model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.db import models
from superadmin.subapps.media_and_groupings import models as samg_models
#from vendor.subapps.profile.models import VendorProfile
from django.utils import timezone

from common.CustomLimitOffsetPaginator import genarate_rand_sting

# Create your models here.

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
    ("ACTIVITY_COVERIMAGE", "ACTIVITY_COVERIMAGE"),
    ("MEDIA_FILE", "MEDIA_FILE"),
)

ACTIVITY_TYPES = (
    ("Day Access", "Day Access"),
    ("Fixed Time", "Fixed Time"),
    ("Open Activity", "Open Activity"),
    ("Term Activity", "Term Activity"),
)

BOOKING_CONFIRMATION = (
    ('5min', '5min'), ('10min', '10min'), ('15min',
                                           '15min'), ('30min', '30min'), ('First', 'First')
)

CUT_OFF_UNIT = (('hours', 'hours'), ('days', 'days'))


class Media(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Media"

    def __str__(self):
        return str(self.name)


class Banner(models.Model):
    banner = models.ForeignKey(
        'Activity', null=True, blank=True, on_delete=models.PROTECT, related_name="banner")
    filepath = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.filepath)

    def save(self, *args, **kwargs):
        return super(Banner, self).save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, unique=True)
    weightage = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'categories'


class SubCategory(models.Model):
    name = models.CharField(max_length=30, default='')
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name='subCategory', blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'subcategories'

    def __str__(self):
        return self.name



def genarate_activiity_code():
    while True:
        code = genarate_rand_sting(3)
        try:
            Activity.objects.get(code=code)
        except Activity.DoesNotExist:
            return code


class Activity(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    code = models.CharField(max_length=10, null=True, blank=True)
    activitytype = models.CharField(
        choices=ACTIVITY_TYPES, max_length=20, null=True, blank=True)
    noofsessions = models.IntegerField(null=True, blank=True)
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,related_name="activities")
    subCategory=models.ForeignKey(SubCategory,on_delete=models.SET_NULL,null=True,blank=True,related_name="activities")
    allowenrollment = models.BooleanField(default=False, null=True, blank=True)
    sessionenrollment = models.CharField(max_length=20, null=True, blank=True)
    coverimage = models.TextField(null=True, blank=True)
    teacherstudentratio = models.CharField(
        max_length=30, null=True, blank=True)
    cutoffunit = models.CharField(
        choices=CUT_OFF_UNIT, max_length=20, null=True, blank=True)
    cutoffvalue = models.IntegerField(null=True, blank=True)
    proratapricing = models.BooleanField(default=False, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    maxstudent = models.CharField(max_length=5, null=True, blank=True)
    freetext = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    evaluation = models.BooleanField(default=False)
    certificate = models.BooleanField(default=False)
    restrictionsguidlines = models.TextField(null=True, blank=True)
    isRegisterationFees = models.BooleanField(default=False)
    isMaterialFees = models.BooleanField(default=False)
    registrationfee = models.IntegerField(null=True, blank=True)
    materialfee = models.IntegerField(null=True, blank=True)
    isVendorNote = models.BooleanField(default=False)
    vendornote = models.TextField(null=True, blank=True)
    chat = models.BooleanField(default=False)
    trial = models.BooleanField(default=False)
    rescheduling = models.BooleanField(default=False)
    cancellation = models.BooleanField(default=False)
    publishevent = models.BooleanField(default=True)
    bookingConfirmation = models.BooleanField(null=True, blank=True)
    bookingtime = models.CharField(max_length=10, null=True, blank=True)
    acttitle = models.CharField(max_length=30, null=True, blank=True)
    guidelines = models.CharField(max_length=100, null=True, blank=True)
    tierpricing = models.BooleanField(default=False)
    tierPricingcheckbox1 = models.BooleanField(default=False)
    tierdescription1 = models.CharField(max_length=20, null=True, blank=True)
    tierPricingcheckbox2 = models.BooleanField(default=False)
    tierdescription2 = models.CharField(max_length=20, null=True, blank=True)
    tierPricingcheckbox3 = models.BooleanField(default=False)
    tierdescription3 = models.CharField(max_length=20, null=True, blank=True)
    message = models.TextField(blank=True, null=True)

    vendor=models.ForeignKey('vendor.VendorProfile',on_delete=models.CASCADE,null=True,blank=True)

    updated_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="vendor_activities")
    updated_at = models.DateTimeField(auto_now=True)
    


class Attribute(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, unique=True)

    class Meta:
        verbose_name_plural = 'attributes'


class SubAttribute(models.Model):
    name = models.CharField(max_length=30, default='')
    attribute = models.ForeignKey(
        'Attribute', on_delete=models.CASCADE, related_name='subAttribute', blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class ActivityAgeGroups(models.Model):
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name='activityAgeGroups',null=True,blank=True)
    
    agegroup=models.ForeignKey(
        samg_models.AgeGroup,on_delete=models.CASCADE, related_name='activityAgeGroups',null=True,blank=True)
    

class ActivitySubAttributes(models.Model):
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name='attributesList',null=True,blank=True)
    
    subAttribute = models.ForeignKey(
        SubAttribute,on_delete=models.CASCADE,related_name="activitySubAttr",null=True,blank=True)
    


class ActivityAttributeGroups(models.Model):
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name='activityAttr')
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name='activityAttr')




class Slot(models.Model):
    # Day access
    activity = models.ForeignKey(
        "Activity", related_name="activity_slots", on_delete=models.PROTECT, blank=True, null=True)
    location = models.ForeignKey(
        "VendorLocation", related_name="activity_loc_slots", on_delete=models.PROTECT, blank=True, null=True)
    slotdate = models.DateField(blank=True, null=True)
    # Date on wich it will start accepting Enrollments
    publishdate = models.DateField(blank=True, null=True)
    totalenrolled = models.PositiveIntegerField(
        null=True, blank=True)         # Slots used
    totalavailableslots = models.PositiveIntegerField(
        null=True, blank=True)   # Total slots
    price = models.PositiveIntegerField(null=True, blank=True)
    tier1pricing = models.PositiveIntegerField(null=True, blank=True)
    tier2pricing = models.PositiveIntegerField(null=True, blank=True)
    tier3pricing = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ('slotdate', )


class Fixedtimingslot(models.Model):
    activity = models.ForeignKey(
        "Activity", related_name="ftslots", on_delete=models.PROTECT, blank=True, null=True)
    location = models.ForeignKey("VendorLocation", related_name="ftlocations", on_delete=models.PROTECT, blank=True,
                                 null=True)
    slotdate = models.DateField(blank=True, null=True)
    # Date on which it will start accepting Enrollments
    publishdate = models.DateField(blank=True, null=True)
    totalenrolled = models.PositiveIntegerField(
        null=True, blank=True)  # Slots used
    totalavailableslots = models.PositiveIntegerField(
        null=True, blank=True)  # Total slots


class Timeslot(models.Model):
    slot = models.ForeignKey(
        "Fixedtimingslot", related_name="timeslots", on_delete=models.PROTECT)
    from_time = models.TimeField(blank=True, null=True)
    to_time = models.TimeField(blank=True, null=True)
    price = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ('from_time', )


REVIEWSTATUS = (
    ('ACTIVE', 'ACTIVE'),  # Reinstate_all = ACTIVE
    # NEED DISCUSSTION WITH JYOTI
    ('REINSTATE_VENDOR_RESPONSE', 'REINSTATE_VENDOR_RESPONSE'),
    ('HIDE', 'HIDE'),  # HIDE_all = HIDE
    ('HIDE_VENDOR_RESPONSE', 'HIDE_VENDOR_RESPONSE')

)


class Reviews(models.Model):
    review = models.TextField(blank=True)
    ratings = models.PositiveIntegerField(default=0)
    response = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=REVIEWSTATUS,
                              default='ACTIVE', max_length=25)


class TermActivity(models.Model):
    activity = models.ForeignKey(
        "Activity", related_name="slots", on_delete=models.PROTECT, blank=True, null=True)
    location = models.ForeignKey(
        "VendorLocation", related_name="slots", on_delete=models.PROTECT, blank=True, null=True)
    name = models.TextField()
    classid = models.TextField(blank=True, null=True)
    publishdate = models.DateField(blank=True, null=True)
    commencementdate = models.DateField(blank=True, null=True)
    totalenrolled = models.TextField(blank=True, null=True)
    totalavailable = models.TextField(blank=True, null=True)
    price = models.PositiveIntegerField(blank=True, null=True)


class TermActivitySlot(models.Model):
    slot = models.ForeignKey("TermActivity", related_name="term_slot",
                             on_delete=models.PROTECT, blank=True, null=True)
    sessionid = models.TextField(blank=True, null=True)
    slotdate = models.DateField(blank=True, null=True)
    sttime = models.TimeField(blank=True, null=True)
    edtime = models.TimeField(blank=True, null=True)

    class Meta:
        ordering = ('slotdate',)


