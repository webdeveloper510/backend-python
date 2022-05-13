from functools import partial
from rest_framework.response import Response
from rest_framework import permissions, serializers, status
from rest_framework.views import APIView
from django.http import HttpResponse
import csv

from common.CustomLimitOffsetPaginator import CustomLimitOffsetPaginator


from .serializers import CouponsSerializer, CouponsParticipantsSerializer
from .models import Coupons, STATUS, CouponsParticipants


class CouponsCSV(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request):
        all_coupons = Coupons.objects.filter(
            created_by=request.user, deleted=False)
        # objs = models.Family.objects.all()
        all_coupons = CouponsSerializer(all_coupons,many=True).data
        response = HttpResponse(content_type='text/csv')
        # force download
        file_name = "Coupons.csv"
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(file_name)
        # the csv writer
        writer = csv.writer(response)

        titles = ['id', 'activity_title', 'activity_code', 'coupon_code', 'discount_value', 'start_date',
                  'discountType', 'end_date', 'total_coupons', 'coupons_used', 'status', 'first_name',
                  'last_name', 'created_at', 'redeemed'
                  ]


        writer.writerow(titles)

        for obj in all_coupons:
            row=[]
            for title in titles:
                row.append(obj[title])
            writer.writerow(row)

        return response


class CouponsViews(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        all_coupons = Coupons.objects.filter(
            created_by=request.user, deleted=False)
        paginator = CustomLimitOffsetPaginator()
        if 'status' in request.query_params:
            sts = request.query_params.get('status')
            all_coupons = all_coupons.filter(status=sts)

        page = paginator.paginate_queryset(all_coupons, request, view=self)
        serializer = serializer = CouponsSerializer(page, many=True)
        if page is not None:
            return paginator.get_paginated_response(serializer.data)

        return Response(serializer.data)

    def post(self, request):
        serializer = CouponsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data)


class CouponViews(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        try:
            coupon = Coupons.objects.get(id=id, deleted=False)
        except Coupons.DoesNotExist as e:
            return Response({'id': 'Does not found coupons'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CouponsSerializer(coupon)

        return Response(serializer.data)

    def patch(self, request, id):
        try:
            coupon = Coupons.objects.get(id=id)
        except Coupons.DoesNotExist as e:
            return Response({'id': 'Does not found coupons'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CouponsSerializer(coupon, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        try:
            coupon = Coupons.objects.get(id=id)
        except Coupons.DoesNotExist as e:
            return Response({'id': 'Does not found coupons'}, status=status.HTTP_404_NOT_FOUND)

        coupon.deleted = True
        coupon.save()
        return Response({'coupon': 'Coupon deleted successful.'}, status=status.HTTP_204_NO_CONTENT)


class ChangeStatus(APIView):
    permission_class = [permissions.IsAuthenticated]

    def get(self, request, id, status_name):
        print('called')
        try:
            coupon = Coupons.objects.get(id=id, deleted=False)
        except Coupons.DoesNotExist as e:
            return Response({'id': 'Does not found coupons'}, status=status.HTTP_404_NOT_FOUND)
        current_status = coupon.status

        if current_status == 'EXPIRED':
            return Response({'success': False, 'status': 'Activity is already expired. So there can not happen any status change.'}, status=status.HTTP_400_BAD_REQUEST)

        if status_name in dict(STATUS).keys() or status_name == 'REINSTATE':

            if current_status == 'SCHEDULED':
                if status_name == 'SUSPENDED':
                    coupon.status = status_name
                    coupon.save()
                    serializer = CouponsSerializer(coupon)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({'success': False, 'message': 'Only you can suspend the coupon'}, status=status.HTTP_400_BAD_REQUEST)

            elif current_status == 'ACTIVE':
                if status_name == 'SUSPENDED':
                    coupon.status = status_name
                    coupon.save()
                    serializer = CouponsSerializer(coupon)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({'success': False, 'message': 'Only you can suspend the coupon'}, status=status.HTTP_400_BAD_REQUEST)

            elif current_status == 'SUSPENDED':
                checked_status = coupon.checkIsStarted()
                if status_name == 'REINSTATE' and checked_status:
                    coupon.status = checked_status
                    coupon.save()
                    serializer = CouponsSerializer(coupon)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({'success': False, 'message': 'Activity is expired or continuing. So you can not reinstate it.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'success': False, 'status': 'This is not a valid status'}, status=status.HTTP_400_BAD_REQUEST)


class CouponsParticipantsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request,code):
        result_data = CouponsParticipants.objects.filter(
            coupon__created_by=request.user,
            coupon__coupon_code=code,
            coupon__deleted=False)
        paginator = CustomLimitOffsetPaginator()
        page = paginator.paginate_queryset(result_data, request, view=self)
        serializer = serializer = CouponsParticipantsSerializer(
            page, many=True)
        if page is not None:
            return paginator.get_paginated_response(serializer.data)

        return Response(serializer.data)
