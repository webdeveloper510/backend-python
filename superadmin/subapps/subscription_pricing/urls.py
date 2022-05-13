from rest_framework.routers import DefaultRouter
from django.urls import path

from . import views_subscriptionpricing as vsp
from . import views_vendorsubscription as vvs

# for namespace. it is important to avoid name problems in {% url %}
app_name = 'subscription_pricing'
'''
=======================================================
sample reverse lookup string for nested namespaces:
=======================================================
reverse('superadmin:subscription_pricing:GetPlansByCountry')
'''

router = DefaultRouter()
router.register('VendorSubscription',vvs.VendorSubscriptions,basename="VendorSubscription")


# Subscription Pricing URLs
urlpatterns = [
    path('subscription_packages/types', vsp.subscription_types.as_view(), name='subscription_types'),
    path('subscription_packages', vsp.subscriptionPackage.as_view(), name='subscription_types'),
    path('subscription_packages/<int:id>', vsp.subscription_package.as_view(), name='UpdateSubscriptionPlans'),
    path('subscription_packages/country/<str:country_name>', vsp.GetPlansByCountry.as_view(), name='GetPlansByCountry'),
    path('subscription_packages/country/<str:country_name>/CSV', vsp.GetPlansByCountryCSV.as_view(), name='SubscriptionPricingCSV'),
]

# Vendor Subscription URLs
urlpatterns += router.urls
