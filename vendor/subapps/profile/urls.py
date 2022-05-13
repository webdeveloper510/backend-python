from os import name
from django.urls import path,include
from . import views

# for namespace. it is important to avoid name problems in {% url %}
app_name = 'vendorlocations'

urlpatterns = [
    path('vendorlocations', views.VendorLocation.as_view(), name='vendorlocation' ),
    path('vendorlocations/<int:id>', views.VendorLocationid.as_view(), name='vendorlocationid'),
    path('vendor/changePassword',views.ChangePasswordView.as_view(),name="change_password"),
    path('vendor/changeName',views.ChangeNameView.as_view(),name="change_name"),
    path('vendor/Profile',views.VendorProfileView.as_view(),name="vendor_profile"),
]