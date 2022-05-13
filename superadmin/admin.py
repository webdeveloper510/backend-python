from django.contrib import admin

# Register your models here.
from django.contrib import admin

from superadmin.subapps.subscription_pricing import models as models_subscription
from superadmin.subapps.countries_and_cities import models as models_country
from superadmin.subapps.vendor_and_user_management import models as models_vendor_user
from superadmin.subapps.media_and_groupings import models as models_media
from superadmin.subapps.receipt import models as models_receipt
from superadmin.subapps.static_info import models as models_static
from superadmin.subapps.vendor_and_user_management import models as models_vendor_and_user_management
from superadmin.subapps.settings import models as models_settings
from superadmin.subapps.revenue import models as revenue_models


from django.contrib.admin.models import LogEntry

from . import models

class LogEntryAdmin(admin.ModelAdmin):
    # to have a date-based drilldown navigation in the admin page
    date_hierarchy = 'action_time'

    # to filter the resultes by users, content types and action flags
    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'action_flag',
    ]

# Register your models here.
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(models.DBOperation)
admin.site.register(models.LogRequest)

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('email', 'first_name', 'last_name',)
#     list_filter = ('is_staff', 'is_superuser')
# admin.site.unregister(models.User)
# admin.site.register(models.User, UserAdmin)

''' Register Subscription and Pricing Models '''
admin.site.register(models_subscription.SubscriptionPackage)

admin.site.register(models_subscription.VendorSubscription)





''' Register Country & Cities Models '''
admin.site.register(models_country.Country)
admin.site.register(models_country.City)
admin.site.register(models_country.Region)
admin.site.register(models_country.Area)
admin.site.register(models_country.Currency)
admin.site.register(models_country.Address)


''' Register Vendor & User Management Models '''
admin.site.register(models_vendor_user.Family)
admin.site.register(models_vendor_user.Kid)
# admin.site.register(models_vendor_user.UserDetail)
admin.site.register(models_vendor_user.Vendor)

''' Register Media And Groupings Models '''
admin.site.register(models_media.AgeGroup)

admin.site.register(models_media.Media)
admin.site.register(models_media.Avatar)
admin.site.register(models_media.Marketing)
admin.site.register(models_media.VendorBannerDetails)
admin.site.register(models_media.HeaderDetails)
admin.site.register(models_media.DefaultHeader)
admin.site.register(models_media.AdminBanner)
admin.site.register(models_media.MarketingSettings)
admin.site.register(models_media.MarketingPrice)
admin.site.register(models_media.MarketingGenericPrice)
admin.site.register(models_media.MarketingWordDetail)
admin.site.register(models_media.SearchWordPricing)
admin.site.register(models_media.SearchWordDetail)



admin.site.register(revenue_models.Coupons)
admin.site.register(revenue_models.couponRedemptionDetails)



''' Register Receipt Models '''
admin.site.register(models_receipt.ReceiptConfig)

''' Register Static Info Models '''
admin.site.register(models_static.StaticResource)

''' Register Vendor Details Models '''
admin.site.register(models_vendor_and_user_management.VendorDetails)

''' Register Settings Models '''
admin.site.register(models_settings.UserFeedback)
admin.site.register(models_settings.UserAdminInvitation)