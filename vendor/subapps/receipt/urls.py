from django.urls import path
from . import views


app_name = 'vendor_reports'

urlpatterns = [
    path('vendor/recepts', views.ReceptsViews.as_view(), name='vendorRecepts'),
    path('vendor/viewReceipt',views.receipt,name='viewReceipt')
]
