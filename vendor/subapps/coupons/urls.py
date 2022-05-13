from django.urls import path
from . import views


app_name = 'vendor_coupons'

urlpatterns = [
    path('vendor/coupons/', views.CouponsViews.as_view(), name='coupons'),
    path('vendor/coupon/<int:id>/', views.CouponViews.as_view(), name='coupon'),
    path('vendor/coupon/<int:id>/<str:status_name>',
         views.ChangeStatus.as_view(), name='statusChange'),
    path('vendor/couponsParticipants',views.CouponsParticipantsView.as_view(),name="couponsParticipants")
]
