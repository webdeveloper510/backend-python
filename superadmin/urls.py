
from django.urls import path, include
# from superadmin.subscription_pricing import views_subscriptionpricing as vsp

# for namespace. it is important to avoid name problems in {% url %}
app_name = 'superadmin'


urlpatterns = [
    path('', include('superadmin.subapps.countries_and_cities.urls',
         namespace='countries_and_cities')),
    path('', include('superadmin.subapps.media_and_groupings.urls',
         namespace='media_and_groupings')),
    path('', include('superadmin.subapps.subscription_pricing.urls',
         namespace='subscription_pricing')),
    path('', include('superadmin.subapps.static_info.urls', namespace='static_info')),
    path('', include('superadmin.subapps.vendor_and_user_management.urls',
         namespace='vendor_and_user_management')),
    path('', include('superadmin.subapps.settings.urls', namespace='settings')),
    path('', include('superadmin.subapps.revenue.urls', namespace='revenue')),
    path('', include('superadmin.subapps.perticipents.urls', namespace='perticipants')),
]
