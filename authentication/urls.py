from django.urls import path
from authentication import vendorViews, views
from .vendorViews import activityVendorView,vendorDateApi,useractivityVendorView
from .views import RegisterView, LogoutAPIView, SetNewPasswordAPIView, VerifyEmail, LoginAPIView,statuscheck, PasswordTokenCheckAPI, RequestPasswordResetEmail,check,activityView,unactivityView
from rest_framework_simplejwt.views import (
    TokenRefreshView,

)
app_name="authentication"

urlpatterns = [
     #search Api
#     path('searchapi',searchViews.as_view(),name="searchapi"),
    path('register/', RegisterView.as_view(), name="register"),
    path('check/', check.as_view(),name="check"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),

    path('activity', activityView.as_view(),
         name='activity'), 
#     path('atcheck', datacheck.as_view(),name='atcheck'),
    path('unactivity',unactivityView.as_view(),name='unactivity'),
    path('vendorActivity', views.vendorActivity,
         name='vendorActivity'),
    path('atcheck', statuscheck.as_view(),
         name='atcheck'),  
#     path('onlycheckuser',onlycheckuser.as_view(),name='onlycheckuser'), 
    path('datecheckuse', views.onlycheckuser,
         name='datecheckuse'), 
    path('searcheng',views.searcheng,
         name="searcheng"),     
    path('response', views.download_file,
         name='response'),
    path('vendorActivitySearch', views.vendorActivitySearch,
         name='vendorActivitySearch'),     

#vendor API 
   path('vendorsearch', vendorViews.onlycheckuser,
         name='vendorsearch'), 
   path('activityVendorView', activityVendorView.as_view(),
         name='activityVendorView'),    

   path('onlycheckuser', vendorViews.onlycheckuser,
         name='onlycheckuser'),         
  


   path('useractivityVendorView', useractivityVendorView.as_view(),
         name='useractivityVendorView'),


    

    
]

