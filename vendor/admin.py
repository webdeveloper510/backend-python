from django.contrib import admin
from vendor.subapps.activity_management import models as models_activity
from vendor.subapps.profile import models as vendors_location
from vendor.subapps.perticipants import models as pertcipant_model
from vendor.subapps.coupons import models as cp_model 
from vendor.subapps.receipt import models as recept_model
#from vendor.subapps.booking import models as booking_model


admin.site.register(models_activity.Activity)
admin.site.register(models_activity.Reviews)
admin.site.register(models_activity.Slot)
admin.site.register(vendors_location.VendorLocation)
admin.site.register(pertcipant_model.Perticipants)
admin.site.register(pertcipant_model.TrialClass)
admin.site.register(pertcipant_model.EvaluationList)
admin.site.register(models_activity.TermActivity)
admin.site.register(models_activity.Media)
admin.site.register(models_activity.ActivityAttributeGroups)
admin.site.register(models_activity.TermActivitySlot)
admin.site.register(models_activity.Fixedtimingslot)
admin.site.register(models_activity.Timeslot)
admin.site.register(models_activity.ActivitySubAttributes)
admin.site.register(cp_model.Coupons)
admin.site.register(cp_model.CouponsParticipants)
admin.site.register(recept_model.Receipt)
#admin.site.register(booking_model.Booking)
admin.site.register(models_activity.Attribute)
admin.site.register(models_activity.SubAttribute)
admin.site.register(models_activity.Category)
admin.site.register(models_activity.SubCategory)
admin.site.register(vendors_location.VendorProfile)
