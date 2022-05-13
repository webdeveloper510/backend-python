from django.urls import path
from . import views

# for namespace. it is important to avoid name problems in {% url %}
app_name = 'vendor_and_user_management'

# Vendor URLs
urlpatterns = [
    path('vendors', views.Vendors.as_view(), name='Vendors'),
    path('vendors/CSV', views.VendorsCSV.as_view(), name='VendorsCSV'),
    path('vendor/<int:id>', views.Vendor.as_view(), name='Vendordetails'),
]

# User URLs
urlpatterns += [
    # for currently logged-in user
    path('user/change_password', views.ChangePassword.as_view(), name='ChangePassword'),
    path('user/profile', views.CurrentUserProfile.as_view(), name='currentuserprofile'),
    path('user/family', views.CurrentUserFamily.as_view(), name='currentuserfamily'),
    path('user/family/kids', views.CurrentFamilyKids.as_view(), name='CurrentFamilyKids'),
    path('user/family/kids/<int:id>', views.CurrentFamilyKid.as_view(), name='CurrentFamilyKid'),

    # for all users
    path('users', views.Users.as_view(), name='userdetails'),
    # path('users/<int:id>', views.User.as_view(), name='userdetails'),
    path('users/<int:id>/profile', views.UserProfile.as_view(), name='userprofile'),
    path('users/families', views.Families.as_view(), name='failies'),
    path('users/families/changeStatus/<int:id>', views.ChangeFamilyStatus.as_view(), name='failies'),
    path('users/families/csv', views.FamiliesCSV.as_view(), name='familiescsv'),
]
