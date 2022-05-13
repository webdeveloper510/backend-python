from django.contrib.auth import get_user_model
User = get_user_model()
from django.db import models
# Create your models here.

STATUS = (
    ("1", "ACTIVE"),
    ("2", "INACTIVE"),
)

class ReceiptConfig(models.Model):
    city = models.OneToOneField('City', on_delete=models.PROTECT, related_name='receiptconfig', null=True, blank=True)
    tax_name = models.CharField(max_length=255, blank=True, null=True)
    tax_rate = models.PositiveIntegerField()
    prices_include_tax = models.BooleanField()
    