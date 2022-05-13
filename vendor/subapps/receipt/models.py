from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from vendor.subapps.activity_management.models import Activity


""" class Receipt(models.Model):
    city = models.ForeignKey('superadmin.City', on_delete=models.CASCADE)
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    businessName = models.CharField(max_length=100)
    businessAddress = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    hasBusinessRegistrationNumber = models.BooleanField(default=False)
    businessRegistrationNumber = models.CharField(
        max_length=25, blank=True, null=True)
    hasPrefix = models.BooleanField(default=False)
    prefix = models.CharField(max_length=25, blank=True, null=True)
    hasTax = models.BooleanField(default=False)
    taxName = models.CharField(max_length=25, blank=True, null=True)
    taxRate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    hasTaxRegistrationNumber = models.BooleanField(default=False)
    taxRegistrationNumber = models.CharField(
        max_length=25, blank=True, null=True)
    agreeMentForTax = models.BooleanField(default=False)
    newTaxName = models.CharField(max_length=25, blank=True, null=True)
    newTaxRate = models.DecimalField(
        max_digits=4, decimal_places=2, blank=True, null=True)
    newTaxApplyDate = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
 """

class Receipt(models.Model):
     #booking = models.ForeignKey('vendor.Booking',on_delete=models.CASCADE)
     receiptNo = models.CharField(max_length=100) 