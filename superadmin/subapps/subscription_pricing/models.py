from django.contrib.auth import get_user_model
from django.db import models
from django.utils import translation

from vendor.subapps.activity_management import models as models_activity
from datetime import datetime,  timedelta

User = get_user_model()

DECIMAL_PLACES = 2  # only applicable to methods. for model fields, change manually and migrate

def checkLeapYear(year):
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


# Create your models here.
SUBSCRIPTION_TYPE = (
    ("BASIC", "BASIC"),
    ("ADVANCED", "ADVANCED"),
    ("PREMIUM", "PREMIUM"),
    ("ENTERPRISE", "ENTERPRISE"),
    ("CUSTOM", "CUSTOM"),
)


class SubscriptionPackage(models.Model):
    subscription_type = models.CharField(max_length=10, choices=SUBSCRIPTION_TYPE, null=True, blank=True)
    price_per_month = models.DecimalField(decimal_places=2, max_digits=13, null=True, blank=True)
    price_per_year = models.DecimalField(decimal_places=2, max_digits=13, null=True, blank=True)
    country = models.ForeignKey('Country', on_delete=models.PROTECT, related_name='subscriptionpackages', null=True, blank=True)

    no_of_locations = models.IntegerField(null=True, blank=True)
    no_of_subadmins = models.IntegerField(null=True, blank=True)
    no_of_media = models.IntegerField(null=True, blank=True)
    has_trial_class = models.BooleanField(null=True, blank=True)
    has_promotions = models.BooleanField(null=True, blank=True)
    has_reports = models.BooleanField(null=True, blank=True)
    has_dashboard = models.BooleanField(null=True, blank=True)
    has_term_renewal = models.BooleanField(null=True, blank=True)
    baner_credit = models.IntegerField(null=True, blank=True)
    header_credit = models.IntegerField(null=True, blank=True)
    search_word_credit = models.IntegerField(null=True, blank=True)

    term_no_of_activities = models.IntegerField(null=True,blank=True)
    term_slots_per_session = models.IntegerField(null=True,blank=True)
    term_sessions_per_term = models.IntegerField(null=True,blank=True)
    term_pricing = models.DecimalField(max_digits=13,decimal_places=2,null=True,blank=True)

    open_no_of_activities = models.IntegerField(null=True,blank=True)
    open_slots_per_session = models.IntegerField(null=True,blank=True)
    open_sessions_per_term = models.IntegerField(null=True,blank=True)
    open_pricing = models.DecimalField(max_digits=13,decimal_places=2,null=True,blank=True)

    day_access_no_of_activities = models.IntegerField(null=True,blank=True)
    day_access_slots_per_session = models.IntegerField(null=True,blank=True)
    day_access_pricing = models.DecimalField(max_digits=13,decimal_places=2,null=True,blank=True)

    fixed_no_of_activities = models.IntegerField(null=True,blank=True)
    fixed_slots_per_session = models.IntegerField(null=True,blank=True)
    fixed_pricing = models.DecimalField(max_digits=13,decimal_places=2,null=True,blank=True)


    def __str__(self):
        # return self.get_name_display() + " - " + str(self.country)
        if (self.subscription_type):
            return self.get_subscription_type_display()
        else:
            return "Subscription Package"


VENDOR_SUBSCRIPTION_STATUS = (
    ("SENT", "SENT"),
    ("CURRENT", "CURRENT"),
    ("EXPIRED", "EXPIRED"),
    # ("INACTIVE", "INACTIVE"),
# used to keep track of subscription history. custom subscriptions wont be deleted from database
)
SUBSCRIPTION_CYCLE_TYPE = (
    ("MONTHLY", "MONTHLY"),
    ("YEARLY", "YEARLY"),
)

class VendorCustomSubscription(models.Model):
    vendor = models.OneToOneField(User, on_delete=models.PROTECT, related_name="custom_vendor_subscription", null=True,blank=True)
    subscription = models.ForeignKey("SubscriptionPackage", on_delete=models.PROTECT, related_name="CustomPackage", null=True, blank=True)

    term_no_of_activities = models.IntegerField(null=True,blank=True)
    term_slots_per_session = models.IntegerField(null=True,blank=True)
    term_sessions_per_term = models.IntegerField(null=True,blank=True)
    term_pricing = models.DecimalField(max_digits=13,decimal_places=2,null=True,blank=True)

    open_no_of_activities = models.IntegerField(null=True,blank=True)
    open_slots_per_session = models.IntegerField(null=True,blank=True)
    open_sessions_per_term = models.IntegerField(null=True,blank=True)
    open_pricing = models.DecimalField(max_digits=13,decimal_places=2,null=True,blank=True)

    day_access_no_of_activities = models.IntegerField(null=True,blank=True)
    day_access_slots_per_session = models.IntegerField(null=True,blank=True)
    day_access_pricing = models.DecimalField(max_digits=13,decimal_places=2,null=True,blank=True)

    fixed_no_of_activities = models.IntegerField(null=True,blank=True)
    fixed_slots_per_session = models.IntegerField(null=True,blank=True)
    fixed_pricing = models.DecimalField(max_digits=13,decimal_places=2,null=True,blank=True)

    


class VendorSubscription(models.Model):
    vendor = models.OneToOneField(User, on_delete=models.PROTECT, related_name="vendor_subscription", null=True,
                               blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    new_billing_date = models.DateTimeField(null=True, blank=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    subscription = models.ForeignKey("SubscriptionPackage", on_delete=models.PROTECT,
                                     related_name="vendor_subscription", null=True, blank=True)

    term_no_of_activities = models.IntegerField(null=True,blank=True)
    term_slots_per_session = models.IntegerField(null=True,blank=True)
    term_sessions_per_term = models.IntegerField(null=True,blank=True)
    term_pricing = models.DecimalField(max_digits=13,decimal_places=2,null=True,blank=True)

    open_no_of_activities = models.IntegerField(null=True,blank=True)
    open_slots_per_session = models.IntegerField(null=True,blank=True)
    open_sessions_per_term = models.IntegerField(null=True,blank=True)
    open_pricing = models.DecimalField(max_digits=13,decimal_places=2,null=True,blank=True)

    day_access_no_of_activities = models.IntegerField(null=True,blank=True)
    day_access_slots_per_session = models.IntegerField(null=True,blank=True)
    day_access_pricing = models.DecimalField(max_digits=13,decimal_places=2,null=True,blank=True)

    fixed_no_of_activities = models.IntegerField(null=True,blank=True)
    fixed_slots_per_session = models.IntegerField(null=True,blank=True)
    fixed_pricing = models.DecimalField(max_digits=13,decimal_places=2,null=True,blank=True)

    # total_amount_paid is always considerd as inclusive of tax [Revenue]
    total_amount_paid = models.DecimalField(decimal_places=2, max_digits=13, null=True, blank=True)
    applied_tax_rate = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True)

    cycle_type = models.CharField(choices=SUBSCRIPTION_CYCLE_TYPE, max_length=10, null=True, blank=True)
    status = models.CharField(choices=VENDOR_SUBSCRIPTION_STATUS, max_length=10, null=True, blank=True)
    email_sent_at = models.DateTimeField(blank=True, null=True)
    # translation_id = models.CharField(max_length=20, blank=True, null=True)

    def get_total_subscription_remaining(self):
        if (self.start_date.date() <= datetime.now().date() <= self.end_date.date()):
            delta = self.end_date.date() - datetime.now().date()
            days_in_year = 366 if checkLeapYear(datetime.now().year) else 365
            return round(float(delta.days) / float(days_in_year) * (float(self.subscription.price_per_month) * 12) , DECIMAL_PLACES)
        else:
            return -1

    def get_total_subscription_payable(self,newPrice=None):
        newPrice = newPrice if newPrice is not None else self.subscription.price_per_month
        if (self.start_date.date() <= datetime.now().date() <= self.end_date.date()):
            delta = datetime.now().date() - self.start_date.date()
            days_in_year = 366 if checkLeapYear(datetime.now().year) else 365
            return  round( float(delta.days) / float(days_in_year) * (float(newPrice) * 12) , DECIMAL_PLACES)
        else:
            return -1

    def get_daily_subscription_cost(self):
        if (self.total_amount_paid and self.start_date and self.end_date ):
            per_day_amount = self.total_amount_paid / (self.end_date.date() - self.start_date.date() + timedelta(days=1)).days
            return round(per_day_amount, DECIMAL_PLACES)
        return None 
    
    def get_daily_tax_cost(self):
        if (self.total_amount_paid and self.start_date and self.end_date ):
            per_day_amount = self.total_amount_paid / (self.end_date.date() - self.start_date.date() + timedelta(days=1)).days
            return round(per_day_amount, DECIMAL_PLACES)
        return None 