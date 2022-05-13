from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views_age_groups as vag
from . import views_avatars as vavt
from . import views_marketing as vm
from . import views_marketingpricing as vmp

router = DefaultRouter()
router.register('agegroups',vag.AgeGroups,basename='agegroups')

#router.register()

# for namespace. it is important to avoid name problems in {% url %}
app_name = 'media_and_groupings'

# Age Group URLs
urlpatterns = router.urls

# Avatars URLs
urlpatterns += [
    path('avatars', vavt.Avatars.as_view(), name='avatars'),
    path('avatars/<int:id>', vavt.Avatar.as_view(), name='avatar'),  # delete only
]

# Marketing URLs
urlpatterns += [
    path('marketings', vm.Marketings.as_view(), name='marketings'),
    path('marketings/<int:id>', vm.Marketing.as_view(), name='marketing'),

    path('marketings/settings', vmp.MarketingSettings.as_view(), name='MarketingSettings'),
    path('marketings/pricing', vmp.MarketingPrice.as_view(), name='MarketingPrice'),

    path('banners/<int:id>/action/<str:action>', vm.VendorBannersAction.as_view(), name='Vendor_banners_action'),
    path('vendorbanners', vm.VendorBanners.as_view(), name='vendorbanners'),

    path('superadminbanners', vm.SuperAdminBanners.as_view(), name='superadminbanners'),
    path('superadminbanners/<int:id>', vm.SuperAdminBanner.as_view(), name='superadminbanner'),

    path('homepageheaders/<int:id>/action/<str:action>', vm.HomepageHeaderAction.as_view(), name='homepage_action'),
    path('vendorhomepageheaders', vm.HomepageHeader.as_view(), name='vendorhomepageheaders'),

    path('superadminheaders', vm.SuperAdminHomepageHeaders.as_view(), name='superadminheaders'),
    path('superadminheaders/<int:id>', vm.SuperAdminHomepageHeader.as_view(), name='superadminheader'),
]
