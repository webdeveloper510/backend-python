from django.urls import path
from . import views
from . import coupon_views

# for namespace. it is important to avoid name problems in {% url %}
app_name = 'revenue'

# User URLs
urlpatterns = [
    # Subscription Revenue
    path('revenue/subscription_revenue', views.SubscriptionRevenue.as_view(), name='SubscriptionRevenue'),
    path('revenue/subscription_revenue/csv', views.SubscriptionRevenueCSV.as_view(), name='SubscriptionRevenueCSV'),

    # Advertising Revenue
    path('revenue/advertising_revenue/summary', views.AdvertisingRevenueSummary.as_view(), name='AdvertisingRevenueSummary'),
    path('revenue/advertising_revenue/summary/csv', views.AdvertisingRevenueSummaryCSV.as_view(), name='AdvertisingRevenueSummaryCSV'),
    
    path('revenue/advertising_revenue/banners', views.BannerAdvertisingRevenue.as_view(), name='BannerAdvertisingRevenue'),
    path('revenue/advertising_revenue/banners/csv', views.BannerAdvertisingRevenueCSV.as_view(), name='BannerAdvertisingRevenueCSV'),

    path('revenue/advertising_revenue/search_words', views.SearchWordsAdvertisingRevenue.as_view(), name='SearchWordsAdvertisingRevenue'),
    path('revenue/advertising_revenue/search_words/csv', views.SearchWordsAdvertisingRevenueCSV.as_view(), name='SearchWordsAdvertisingRevenueCSV'),

]


urlpatterns += [
    path('coupons', coupon_views.coupons.as_view(), name="coupons"),
    path('coupon/<int:cid>', coupon_views.coupon.as_view(), name="coupon"),
    path('coupon/<int:cid>/<str:action>', coupon_views.couponStatusChange.as_view(), name="couponAction"),
    path('coupon/vendor/<int:c_id>', coupon_views.addCouponByVebdor.as_view(), name="couponRegister")
]