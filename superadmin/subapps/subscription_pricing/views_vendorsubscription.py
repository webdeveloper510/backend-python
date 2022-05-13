from rest_framework import viewsets,views,mixins,permissions,status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.contrib.auth import get_user_model

User=get_user_model()

from . import serializers_vendorsubscription
from .models import VendorSubscription,VendorCustomSubscription,SubscriptionPackage

class VendorSubscriptions(viewsets.ModelViewSet):
    queryset=VendorSubscription.objects.all()
    serializer_class=serializers_vendorsubscription.VendorSubscriptionSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = VendorSubscription.objects.all()
        country = self.request.query_params.get('country',None)
        if country is not None:
            queryset = queryset.filter(subscription__country__name=country)
            print(queryset)
        type = self.request.query_params.get('type',None)
        if type is not None:
            queryset = queryset.filter(subscription__subscription_type=type)
        status = self.request.query_params.get('status',None)
        if status is not None:
            queryset = queryset.filter(status=status)
        return queryset

    @action(detail=True,methods=['post'])
    def request_upgrade(self,request,pk=None):
        try:
            vs = VendorSubscription.objects.get(pk=pk)
        except VendorSubscription.DoesNotExist:
            return Response({"error":"Vendor Subscription Objects Not Found."},status=status.HTTP_404_NOT_FOUND)
        
        request.data['subscription']['subscription_type'] = 'CUSTOM'
        #print(vs.vendor)
        request.data['vendor'] = vs.vendor.id
        instance = serializers_vendorsubscription.CustomSubscriptionSerializer(data=request.data)

        if instance.is_valid():
            instance.save()
        else:
            return Response(instance.errors,status=status.HTTP_400_BAD_REQUEST)

        vs.status='SENT'
        #TODO Sending Email

        vs.email_sent_at=timezone.now()
        vs.save()

        return Response({"message":"Plan Upgraded Requested Successfully."})
    
    @action(detail=True,methods=['post'])    
    def complete_upgrade(self,request,pk=None):
        try:
            vs = VendorSubscription.objects.get(pk=pk)
        except VendorSubscription.DoesNotExist:
            return Response({"error":"Vendor Subscription Objects Not Found."},status=status.HTTP_404_NOT_FOUND)
        
        custom_subscription = serializers_vendorsubscription.CustomSubscriptionSerializer(vs.vendor.custom_vendor_subscription).data

        custom_subscription.pop('vendor')

        custom_subscription['subscription'] = SubscriptionPackage.objects.get(id=custom_subscription['subscription'].get('id'))

        VendorSubscription.objects.filter(id=pk).update(status='CURRENT',**custom_subscription)

        return Response({"message":"Plan Upgraded Completed Successfully."})
    
    @action(detail=True,methods=['get'])
    def payment_link(self,request,pk=None):
        try:
            vs = VendorSubscription.objects.get(pk=pk)
        except VendorSubscription.DoesNotExist:
            return Response({"error":"Vendor Subscription Objects Not Found."},status=status.HTTP_404_NOT_FOUND)
        
        return Response({"payment_link":"http://paymentgatewaynotyetimplemented.com"})
    
    @action(detail=True,methods=['get'])
    def remaining_payable(self,request,pk=None):
        try:
            vs = VendorSubscription.objects.get(pk=pk)
        except VendorSubscription.DoesNotExist:
            return Response({"error":"Vendor Subscription Objects Not Found."},status=status.HTTP_404_NOT_FOUND)
        
        new_price = request.GET.get('price',None)

        try:
            float(new_price)
        except TypeError:
            return Response({"error":"Send a valid new monthly price as price in query parameter."},status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error":"Send a valid new monthly price as price in query parameter."},status=status.HTTP_400_BAD_REQUEST)

        return Response({"remaining_payable":vs.get_total_subscription_payable(new_price)})

    @action(detail=True,methods=['post'])
    def cancel(self,request,pk=None):
        try:
            vs = VendorSubscription.objects.get(pk=pk)
        except VendorSubscription.DoesNotExist:
            return Response({"error":"Vendor Subscription Objects Not Found."},status=status.HTTP_404_NOT_FOUND)

        try:
            vs.vendor.custom_vendor_subscription.delete()
            vs.status='CURRENT'
            vs.save() 
            #TODO Diaable Payment Link
        except VendorCustomSubscription.DoesNotExist:
            return Response({"error":"There is no custom subscription."},status=status.HTTP_404_NOT_FOUND)
        
        return Response({"message":"Custom Subscription Cancelled Successfully."})
        



