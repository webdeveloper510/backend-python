from django.db import models

class Booking(models.Model):
    vendor = models.ForeignKey('vendor.VendorDetails',on_delete=models.PROTECT)
    participant = models.ForeignKey('vendor.Perticipants',on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    bookingRefNo = models.CharField(max_length=50)

    bookingDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.bookingRefNo
