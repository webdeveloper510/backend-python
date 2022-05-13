from common.CustomLimitOffsetPaginator import CustomLimitOffsetPaginator
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models as Activity_manage_model
from . import reviewSerialzer
from superadmin.subapps.vendor_and_user_management.models import Vendor


class Reviews(APIView):

    def get(self, request):

        all_reviews = Activity_manage_model.Reviews.objects.all()
        if 'vendor_code' in request.query_params:
            try:
                vendor = Vendor.objects.get(
                    vendor_code=request.query_params.get('vendor_code'))
                print(vendor)
            except Vendor.DoesNotExist:
                return Response({'vendor_code': 'This code can\'t found'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            all_reviews = all_reviews.filter(activity__created_by=vendor.user)

        if 'vendor_name' in request.query_params:
            try:
                vendor = [v.user for v in Vendor.objects.filter(
                    name=request.query_params.get('vendor_name'))]

            except Vendor.DoesNotExist:
                return Response({'vendor_name': 'This name can\'t found'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            all_reviews = all_reviews.filter(activity__created_by__in=vendor)

        if 'city' in request.query_params:
            vendor = Vendor.objects.filter(
                city__name=request.query_params.get('city')).values('user')
            all_reviews = all_reviews.filter(activity__created_by__in=vendor)

        # get start date
        if 'first_date' in request.query_params:
            all_reviews = all_reviews.filter(
                created_at__date__gte=request.query_params.get('first_date'))

        # get till date
        if 'last_date' in request.query_params:
            all_reviews = all_reviews.filter(
                created_at__date__lte=request.query_params.get('last_date'))

        if 'stars' in request.GET:
            stars = request.GET.get('stars')

            try:
                if int(stars) > 5:
                    raise ValueError()
            except TypeError:
                return Response({"error":"Not a valid number."},status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({"error":"Not a valid number."},status=status.HTTP_400_BAD_REQUEST)
                
            all_reviews = all_reviews.filter(ratings=stars)

        # IF paginator need
        paginator = CustomLimitOffsetPaginator()

        serializer = reviewSerialzer.ReviewsSerializer(all_reviews, many=True)
        five_star = 0
        four_star = 0
        three_star = 0
        two_star = 0
        one_star = 0
        for review in all_reviews:
            val = round(review.ratings)
            if val == 5:
                five_star += 1
            elif val == 4:
                four_star += 1
            elif val == 3:
                three_star += 1
            elif val == 2:
                two_star += 1
            elif val == 1:
                one_star += 1
        try:
            over_all = ((five_star * 5) + (four_star * 4) + (three_star*3) + (two_star*2) +
                        (one_star*1)) / (five_star + four_star + three_star + two_star + one_star)
        except:
            over_all = 0
        if(request.GET.get(CustomLimitOffsetPaginator.limit_query_param, False)):
            page = paginator.paginate_queryset(all_reviews, request, view=self)
            serializer = reviewSerialzer.ReviewsSerializer(page, many=True)
            if page is not None:
                return paginator.get_paginated_response({"data": serializer.data, 'stars': {'5': five_star, '4': four_star, '3': three_star, '2': two_star, '1': one_star, 'over_all': over_all}})
        return Response({"data": serializer.data, 'stars': {'5': five_star, '4': four_star, '3': three_star, '2': two_star, '1': one_star, 'over_all': over_all}})

    def post(self, request):
        serializer = reviewSerialzer.ReviewsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(
            reviewed_by=request.user if request.user.is_authenticated else None)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Review(APIView):

    def get(self, request, id):
        try:
            review = Activity_manage_model.Reviews.objects.get(id=id)
        except Activity_manage_model.Reviews.DoesNotExist:
            return Response({'error': 'Reviews can not found'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = reviewSerialzer.ReviewsSerializer(review)
        return Response(serializer.data)

    def patch(self, request, id):
        try:
            instance = Activity_manage_model.Reviews.objects.get(id=id)
        except Activity_manage_model.Reviews.DoesNotExist:
            return Response({'error': 'Reviews can not found'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = reviewSerialzer.ReviewsSerializer(
            data=request.data, instance=instance, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        try:
            instance = Activity_manage_model.Reviews.objects.get(id=id)
        except Activity_manage_model.Reviews.DoesNotExist:
            return Response({'error': 'Reviews can not found'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance.delete()
            return Response({'message': "Review deleted successful."})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VendorReviews(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        print('===============')
        print('===============')
        activities = Activity_manage_model.Activity.objects.all()

        if 'title' in request.GET:
            title = request.GET.get('title')
            activities = activities.filter(title=title)

        if 'code' in request.GET:
            code = request.GET.get('code')
            activities = activities.filter(code=code)

        all_reviews = Activity_manage_model.Reviews.objects.filter(
            activity__in=activities).order_by('-created_at')

        if 'first_date' in request.GET:
            from_date = request.GET.get('first_date')
            all_reviews = all_reviews.filter(created_at__gte=from_date)

        if 'last_date' in request.GET:
            from_date = request.GET.get('last_date')
            all_reviews = all_reviews.filter(created_at__lte=from_date)
        
        if 'stars' in request.GET:
            stars = request.GET.get('stars')
            try:
                if int(stars) > 5:
                    raise ValueError()
            except TypeError:
                return Response({"error":"Not a valid number."},status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({"error":"Not a valid number."},status=status.HTTP_400_BAD_REQUEST)
                
            all_reviews = all_reviews.filter(ratings=stars)

        print('I am here')
        serializer = reviewSerialzer.VendorReviewSerializer(
            all_reviews, many=True)

        five_star = 0
        four_star = 0
        three_star = 0
        two_star = 0
        one_star = 0
        for review in all_reviews:
            val = round(review.ratings)
            if val == 5:
                five_star += 1
            elif val == 4:
                four_star += 1
            elif val == 3:
                three_star += 1
            elif val == 2:
                two_star += 1
            elif val == 1:
                one_star += 1
        try:
            over_all = ((five_star * 5) + (four_star * 4) + (three_star*3) + (two_star*2) +
                        (one_star*1)) / (five_star + four_star + three_star + two_star + one_star)
        except:
            over_all = 0
            
        paginator = CustomLimitOffsetPaginator()

        if(request.GET.get(CustomLimitOffsetPaginator.limit_query_param, False)):
            page = paginator.paginate_queryset(all_reviews, request, view=self)
            serializer = reviewSerialzer.ReviewsSerializer(page, many=True)
            if page is not None:
                return paginator.get_paginated_response({"data": serializer.data, 'stars': {'5': five_star, '4': four_star, '3': three_star, '2': two_star, '1': one_star, 'over_all': over_all}})
        return Response({"data": serializer.data, 'stars': {'5': five_star, '4': four_star, '3': three_star, '2': two_star, '1': one_star, 'over_all': over_all}})




class VendorReview(APIView):
    permission_classes = (permissions.IsAuthenticated, )


    def get(self, request, id):
        try:
            review = Activity_manage_model.Reviews.objects.get(id=id,activity__created_by=request.user)
        except Activity_manage_model.Reviews.DoesNotExist:
            return Response({'error': 'Reviews can not found'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = reviewSerialzer.ReviewsSerializer(review)
        return Response(serializer.data)

    def patch(self, request, id):
        try:
            instance = Activity_manage_model.Reviews.objects.get(id=id)
        except Activity_manage_model.Reviews.DoesNotExist:
            return Response({'error': 'Reviews can not found'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = reviewSerialzer.ReviewsSerializer(
            data=request.data, instance=instance, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        try:
            instance = Activity_manage_model.Reviews.objects.get(id=id)
        except Activity_manage_model.Reviews.DoesNotExist:
            return Response({'error': 'Reviews can not found'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance.delete()
            return Response({'message': "Review deleted successful."})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
