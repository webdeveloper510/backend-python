from django.db import models
from superadmin.subapps.media_and_groupings.models import MARKETING_STATUS
from django.conf import settings
User = settings.AUTH_USER_MODEL

DISCOUNTTYPE = (
    ('percent', 'percent'),
    ('value', 'value')
)


class Coupons(models.Model):
    coupon_code = models.CharField(max_length=8)
    discountType = models.CharField(
        choices=DISCOUNTTYPE, max_length=8, default='value')
    discount_value = models.DecimalField(
        max_digits=6, decimal_places=1, default=0)
    country = models.ForeignKey(
        'Country', on_delete=models.CASCADE, related_name='coupons', null=True, blank=True)
    subscriptions = models.ManyToManyField(
        'SubscriptionPackage', related_name='coupons')
    from_date = models.DateField()
    to_date = models.DateField()
    max_number_of_coupon = models.IntegerField(default=0)
    status = models.CharField(choices=MARKETING_STATUS,
                              max_length=15, default='SCHEDULED')
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='coupons', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)


class couponRedemptionDetails(models.Model):
    vendorSubscription = models.ForeignKey(
        'VendorSubscription', on_delete=models.CASCADE)
    coupon = models.ForeignKey(
        'Coupons', on_delete=models.CASCADE, related_name='coupondetails')
