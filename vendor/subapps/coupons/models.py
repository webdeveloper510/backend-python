from datetime import date
from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
from vendor.subapps.activity_management.models import Activity


STATUS = (
    ("ACTIVE", "ACTIVE"),
    ("SCHEDULED", "SCHEDULED"),
    ("SUSPENDED", "SUSPENDED"),
    ("EXPIRED", "EXPIRED"),
)


DISCOUNTTYPE = (
    ('percent', 'percent'),
    ('value', 'value')
)


class Coupons(models.Model):
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name='activity_coupons')
    discountType = models.CharField(
        choices=DISCOUNTTYPE, max_length=8, default='value')
    coupon_code = models.CharField(unique=True, max_length=8)
    discount_value = models.DecimalField(
        decimal_places=2, max_digits=13, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    total_coupons = models.PositiveIntegerField(default=0)
    coupons_used = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='vendorUser')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=STATUS, max_length=15, default='SCHEDULED')
    deleted = models.BooleanField(default=False)

    def checkIsStarted(self):
        today = date.today()
        print('**********', today < self.start_date)
        if today < self.start_date:
            return 'SCHEDULED'
        elif today >= self.start_date and today < self.end_date:
            return 'ACTIVE'
        else:
            return False

class CouponsParticipants(models.Model):
    coupon = models.ForeignKey(Coupons,on_delete=models.CASCADE)
    participant = models.ForeignKey('vendor.Perticipants',on_delete=models.CASCADE)

    created_at =models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

