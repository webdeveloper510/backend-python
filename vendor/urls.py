from django.urls import path, include
# from superadmin.subscription_pricing import views_subscriptionpricing as vsp

# for namespace. it is important to avoid name problems in {% url %}
app_name = 'vendor'


urlpatterns = [
    path('', include('vendor.subapps.activity_management.urls',
         namespace='activity_management')),
    path('', include('vendor.subapps.coupons.urls', namespace='coupons')),
    path('', include('vendor.subapps.perticipants.urls', namespace='perticipants')),
    path('', include('vendor.subapps.profile.urls', namespace='profile')),
    path('', include('vendor.subapps.receipt.urls', namespace='receipt')),
    path('', include('vendor.subapps.revenue.urls', namespace='revenue')),
    path('', include('vendor.subapps.trial_class.urls', namespace='trial_class')),
    path('', include('vendor.subapps.bookings.urls', namespace='bookings')),

]
