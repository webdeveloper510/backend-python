from datetime import datetime, date
from superadmin.subapps.media_and_groupings.models import Marketing
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from common.CustomLimitOffsetPaginator import CustomLimitOffsetPaginator
from superadmin.subapps.subscription_pricing.models import VendorSubscription
from . import models as coupon_model
from . import coupon_serializers
from authentication import responses


class coupons(APIView):

    def get(self, request):
        coupons = coupon_model.Coupons.objects.filter(
            deleted=False).prefetch_related('subscriptions')
        paginator = CustomLimitOffsetPaginator()
        if(request.GET.get(CustomLimitOffsetPaginator.limit_query_param, False)):
            page = paginator.paginate_queryset(coupons, request, view=self)
            serializer = coupon_serializers.CouponSerialzier(
                page, many=True
            )
            if page is not None:
                return paginator.get_paginated_response(serializer.data)
        serializer = coupon_serializers.CouponSerialzier(coupons, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = coupon_serializers.CouponSerialzier(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.is_authenticated:
            serializer.save(created_by=request.user)
        else:
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class coupon(APIView):

    def patch(self, request, cid):
        try:
            coupon = coupon_model.Coupons.objects.get(id=cid, deleted=False)

        except Exception as e:
            print(e)
            return Response({'error': "Coupon not found"}, status=status.HTTP_400_BAD_REQUEST)

        if coupon.status == 'SCHEDULED':
            serializer = coupon_serializers.CouponSerialzier(
                coupon, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        elif coupon.status == 'ACTIVE':
            return Response({"error": "This coupon can not be edit. You can suspend it only."}, status=status.HTTP_400_BAD_REQUEST)

        elif coupon.status == 'EXPIRED':
            return Response({"error": "This coupon can not be edit. You can delete it only."}, status=status.HTTP_400_BAD_REQUEST)

        elif coupon.status == 'SUSPENDED':
            today = date.today()
            # coupon yet to start
            if coupon.from_date > today:
                serializer = coupon_serializers.CouponSerialzier(
                    coupon, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            # if start
            if (coupon.from_date < today) and (coupon.to_date >= today):

                serializer = coupon_serializers.CouponSerialzier(
                    coupon, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            # if expired
            if (coupon.to_date < today):
                return Response({"error": "This coupon can not be edit. You can delete it only."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, cid):
        try:
            coupon = coupon_model.Coupons.objects.get(id=cid)
            coupon.deleted = True
            coupon.save()
            return Response({'message': "Coupon deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        except:
            return Response({'error': "Coupon not found"}, status=status.HTTP_400_BAD_REQUEST)


class couponStatusChange(APIView):

    def get(self, request, cid, action):
        try:
            coupon = coupon_model.Coupons.objects.get(id=cid, deleted=False)
            MARKETING_STATUS = ["ACTIVE", "SCHEDULED", "SUSPENDED", "EXPIRED"]
            if action in MARKETING_STATUS:
                if (coupon.status == 'SCHEDULED' or coupon.status == 'ACTIVE'):
                    if action == 'SUSPENDED':
                        coupon.status = action
                        coupon.save()
                    else:
                        return Response({'error': "This coupon only can do 'SUSPENDED'"}, status=status.HTTP_400_BAD_REQUEST)

                elif coupon.status == 'EXPIRED':
                    return Response({'error': "This coupon can't change status"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    today = date.today()

                    coupon_status = 'EXPIRED'
                    # if coupon yet to start then only action will be 'SCHEDULED'
                    if coupon.from_date > today:
                        coupon_status = 'SCHEDULED'
                    elif coupon.from_date < today and coupon.to_date >= today:
                        coupon_status = 'ACTIVE'
                    print(coupon_status)
                    if coupon_status == 'EXPIRED':
                        return Response({'error': "Coupon has expired. So, there has not any reinstate."}, status=status.HTTP_400_BAD_REQUEST)

                    #  if according to date it will be active, so action need to be active
                    if coupon_status == 'ACTIVE':
                        if action == 'ACTIVE':
                            coupon.status = action
                            coupon.save()
                        else:
                            return Response({'error': "Coupon started. So, only status will be 'ACTIVE' for reinstate."}, status=status.HTTP_400_BAD_REQUEST)

                    if coupon_status == 'SCHEDULED':
                        if action == 'SCHEDULED':
                            coupon.status = action
                            coupon.save()

                        else:
                            return Response({'error': "Coupon does not start yet. So, only status will be 'SCHEDULED' for reinstate."}, status=status.HTTP_400_BAD_REQUEST)

                serializer = coupon_serializers.CouponSerialzier(coupon)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': "status is not a valid options. valid options are " + '/'.join(MARKETING_STATUS)}, status=400)
        except coupon_model.Coupons.DoesNotExist as e:
            print(e)
            return Response({'error': "Coupon not found"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class addCouponByVebdor(APIView):

    def get(self, request, c_id):
        try:
            coupons = coupon_model.couponRedemptionDetails.objects.filter(
                coupon__id=c_id)
            serializer = coupon_serializers.couponRedemptionDetailsSerializer(
                coupons, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except coupon_model.couponRedemptionDetails.DoesNotExist as e:
            return Response(responses.RESP_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request, c_id):
    #     try:
    #         coupons = coupon_model.Coupons.objects.get(id=c_id)
    #         if coupons.max_number_of_coupon ==0: # max_number_of_coupon is 0 then no coupon can applied
    #             return Response(responses.create_failure_response('Coupon is not available'), status=status.HTTP_400_BAD_REQUEST)

    #     except coupon_model.couponRedemptionDetails.DoesNotExist as e:
    #         return Response(responses.create_failure_response('Coupon not found.'), status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         vendorSubscription = request.data['subscription']
    #     except:
    #         return Response({'subscription': 'This field is required'}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         vendorSubs = VendorSubscription.objects.get(id=vendorSubscription)
    #         alreadyExists = coupon_model.couponRedemptionDetails.objects.filter(coupon=coupons, vendorSubscription=vendorSubs).exists()
    #         # If already applied by vendor then return error
    #         if alreadyExists:
    #             return Response({"error": 'This coupon all ready applied.'}, status=status.HTTP_400_BAD_REQUEST)

    #     except VendorSubscription.DoesNotExist:
    #         return Response(responses.create_failure_response('Vendor Subscription not found.'), status=status.HTTP_400_BAD_REQUEST)

    #     couponRedemption = coupon_model.couponRedemptionDetails(coupon=coupons, vendorSubscription=vendorSubs)
    #     couponRedemption.save()
    #     coupons.max_number_of_coupon = coupons.max_number_of_coupon -1
    #     coupons.save()
    #     serializer = coupon_serializers.couponRedemptionDetailsSerializer(couponRedemption)
    #     return Response(serializer.data)
