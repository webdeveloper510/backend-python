from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import serializers_marketing as serializers
from . import models
from superadmin.subapps.countries_and_cities import models as models_country

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from authentication import decorators as auth_decorators
from authentication import responses

# For HTTP Error
from rest_framework import status
from datetime import datetime, timedelta

from django.db.models import ProtectedError
# =======================
#       Methods
# =======================


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
# =======================


class Marketings(APIView):
    # To allow authenticated users only

    def get(self, request):
        obj = models.Marketing.objects.all()
        serializer = serializers.MarketingSerializer(obj, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.MarketingSerializer(data=request.data)
        if(serializer.is_valid()):
            obj = serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Marketing(APIView):
    # To allow authenticated users only

    def get(self, request, id):
        try:
            obj = models.Marketing.objects.get(id=id)
        except:
            return Response(responses.RESP_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.MarketingSerializer(obj)
        return Response(serializer.data)

    def delete(self, request, id):
        try:
            obj = models.Marketing.objects.get(id=id)
        except:
            return Response(responses.RESP_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        try:
            obj.delete()
            return Response(responses.create_success_response('object deleted successfully'))
        
        except ProtectedError as e:
            return Response(responses.create_failure_response('this object is currently being used. ' + str(e) ) )
        
        except:
            return Response(responses.RESP_INTERNAL_SERVER_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, id):
        try:
            obj = models.Marketing.objects.get(id=id)
        except:
            return Response(responses.RESP_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.MarketingSerializer(
            obj, data=request.data,  partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ========================================
#           Vendor Banners
# ========================================

class VendorBannersAction(APIView):
    # To allow authenticated users only

    def get(self, request, id, action):
        try:
            obj = models.Marketing.objects.get(id=id, type="BANNER")
        except:
            return Response(responses.create_failure_response('banner object does not exists'), status=status.HTTP_400_BAD_REQUEST)

        try:
            valid_actions = ['ACTIVATE', 'SUSPEND']
            if(action == "ACTIVATE"):
                obj.status = "ACTIVE"
                obj.save()
                return Response(responses.create_success_response('banner is activated successfully'))

            elif(action == "SUSPEND"):
                obj.status = "SUSPENDED"
                obj.save()
                return Response(responses.create_success_response('banner is suspended successfully'))
            else:
                return Response(responses.create_failure_response('invalid action. valid value are ' + str(valid_actions)), status=status.HTTP_400_BAD_REQUEST)
            pass
        except:
            return Response(responses.RESP_INTERNAL_SERVER_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VendorBanners(APIView):
    # To allow authenticated users only

    def get(self, request):
        objs = models.Marketing.objects.filter(type="BANNER")
        # print(request.GET)
        if('first_date' in request.GET):
            first_date = request.GET.get('first_date')
        else:
            return Response(responses.create_failure_response('parameter first_date is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('last_date' in request.GET):
            last_date = request.GET.get('last_date')
        else:
            return Response(responses.create_failure_response('parameter last_date is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('platform_type' in request.GET):
            platform_type = request.GET.get('platform_type')
            if(platform_type not in dict(models.PLATFORM_TYPE).keys()):
                return Response(responses.create_failure_response('platform_type is not a valid date value'), status=status.HTTP_400_BAD_REQUEST)
            objs = objs.filter(platform_type=platform_type)
            # print(objs)
        else:
            return Response(responses.create_failure_response('parameter platform_type is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('city' in request.GET):
            city = request.GET.get('city')
            try:
                city = get_object_or_404(models_country.City, name=city)
            except:
                return Response(responses.create_failure_response('city object not found'), status=status.HTTP_400_BAD_REQUEST)

            objs = objs.filter(city=city)
        else:
            return Response(responses.create_failure_response('parameter city is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('catagory' in request.GET):
            catagory = request.GET.get('catagory')
            try:
                catagory = get_object_or_404(models.Category, name=catagory)
            except:
                return Response(responses.create_failure_response('catagory object not found'), status=status.HTTP_400_BAD_REQUEST)

            objs = objs.filter(banner_details__catagory__name=catagory.name)
            
        else:
            return Response(responses.create_failure_response('parameter catagory is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        # print(platform_type)
        try:
            first_date = datetime.strptime(first_date, "%Y-%m-%d").date()
        except:
            return Response(responses.create_failure_response('first_date is not a valid date value. please provide date string in format YYYY-MM-DD'), status=status.HTTP_400_BAD_REQUEST)

        try:
            last_date = datetime.strptime(last_date, "%Y-%m-%d").date()
        except:
            return Response(responses.create_failure_response('last_date is not a valid date value. please provide date string in format YYYY-MM-DD'), status=status.HTTP_400_BAD_REQUEST)

        max_count = models.MarketingSettings.objects.filter(
            marketing_type="BANNER", platform_type=platform_type, city=city)
        if(max_count.exists()):
            max_count = max_count.first()
            pass
        else:
            max_count = models.MarketingSettings.objects.create(
                marketing_type="BANNER", platform_type=platform_type, city=city, max_count=5)

        dates = []
        # for single_date in daterange(first_date, last_date):
        delta = timedelta(days=1)
        while first_date <= last_date:
            single_date = first_date
            date = single_date.strftime("%Y-%m-%d")
            banners = objs.filter(
                from_date__lte=single_date,
                to_date__gte=single_date
            )
            # if(banners.count() > max_count.max_count):    # Only for testing
            #     print("max_count exceeded")

            serializer = serializers.BannerMarketingSerializer(
                banners, many=True, context={'platform_type': platform_type})

            obj = {
                "date": date,
                "banners": serializer.data,
            }
            dates.append(obj)
            first_date += delta

        resp = {
            "max_count": max_count.max_count,
            "dates": dates
        }

        return Response(resp)

# ========================================
#           Super Admin Banners
# ========================================


class SuperAdminBanners(APIView):
    # To allow authenticated users only

    def get(self, request):
        objs = models.AdminBanner.objects.all()
        

        if('platform_type' in request.GET):
            platform_type = request.GET.get('platform_type')
            if(platform_type not in dict(models.PLATFORM_TYPE).keys()):
                return Response(responses.create_failure_response('platform_type is not a valid date value'), status=status.HTTP_400_BAD_REQUEST)
            objs = objs.filter(platform_type=platform_type)
        else:
            return Response(responses.create_failure_response('parameter platform_type is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('city' in request.GET):
            city = request.GET.get('city')
            try:
                city = get_object_or_404(models_country.City, name=city)
            except:
                return Response(responses.create_failure_response('city object not found'), status=status.HTTP_400_BAD_REQUEST)

            objs = objs.filter(city=city)
        else:
            return Response(responses.create_failure_response('parameter city is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        max_count = models.MarketingSettings.objects.filter(
            marketing_type="BANNER", platform_type=platform_type, city=city)
        if(max_count.exists()):
            max_count = max_count.first()
            pass
        else:
            max_count = models.MarketingSettings.objects.create(
                marketing_type="BANNER", platform_type=platform_type, city=city, max_count=5)

        cat_list = []
        if('categories' in request.GET):
            categories = request.GET.get('categories')
            categories = categories.split(',')
            # print(categories)
            for category in categories:
                try:
                    cat = get_object_or_404(models.Category, name=category)
                    # print(cat)
                except:
                    return Response(responses.create_failure_response('catagory object not found'), status=status.HTTP_400_BAD_REQUEST)

                banners = objs.filter(category__name=cat.name)
                serializer = serializers.SuperAdminBannerSerializer(
                    banners, many=True)
                obj = {
                    "category": category,
                    "id": category,
                    "banners": serializer.data,
                }
                cat_list.append(obj)
        else:
            categories = set(obj['category'] for obj in objs.values('category'))
            
            for category in categories:
                try:
                    cat = get_object_or_404(models.Category, id=category)
                except:
                    return Response(responses.create_failure_response('catagory object not found'), status=status.HTTP_400_BAD_REQUEST)

                banners = objs.filter(category__name=cat.name)
                if(banners.count() > max_count.max_count):    # Only for testing
                    # print("max_count exceeded")
                    pass
                serializer = serializers.SuperAdminBannerSerializer(
                    banners, many=True)
                # print(category)
                obj = {
                    "category": cat.name,
                    "id": category,
                    "banners": serializer.data,
                }
                cat_list.append(obj)
        resp = {
            "max_count": max_count.max_count,
            "categories": cat_list
        }

        return Response(resp)

    def post(self, request):
        serializer = serializers.SuperAdminBannerSerializer(
            data=request.data, user=request.user)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SuperAdminBanner(APIView):
    # To allow authenticated users only

    def delete(self, request, id):
        try:
            obj = models.AdminBanner.objects.get(id=id)
        except:
            return Response(responses.RESP_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        try:
            obj.delete()
            
            return Response(responses.create_success_response('object deleted successfully'), status=status.HTTP_204_NO_CONTENT)
        
        except ProtectedError as e:
            return Response(responses.create_failure_response('this object is currently being used. ' + str(e) ), status=status.HTTP_400_BAD_REQUEST)
        
        except:
            return Response(responses.RESP_INTERNAL_SERVER_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# =========================================================
#                   Homepage Headers
# =========================================================


class HomepageHeaderAction(APIView):
    # To allow authenticated users only

    def get(self, request, id, action):
        try:
            obj = models.Marketing.objects.get(id=id, type="HEADER")
        except:
            return Response(responses.create_failure_response('homepage header object does not exists'), status=status.HTTP_400_BAD_REQUEST)

        try:
            valid_actions = ['ACTIVATE', 'SUSPEND']
            if(action == "ACTIVATE"):
                obj.status = "ACTIVE"
                obj.save()
                return Response(responses.create_success_response('homepage header is activated successfully'))

            elif(action == "SUSPEND"):
                obj.status = "SUSPENDED"
                obj.save()
                return Response(responses.create_success_response('homepage header is suspended successfully'))
            else:
                return Response(responses.create_failure_response('invalid action. valid value are ' + str(valid_actions)), status=status.HTTP_400_BAD_REQUEST)
            pass
        except:
            return Response(responses.RESP_INTERNAL_SERVER_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HomepageHeader(APIView):
    # To allow authenticated users only

    def get(self, request):
        objs = models.Marketing.objects.filter(type="HEADER")

        if('first_date' in request.GET):
            first_date = request.GET.get('first_date')
        else:
            return Response(responses.create_failure_response('parameter first_date is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('last_date' in request.GET):
            last_date = request.GET.get('last_date')
        else:
            return Response(responses.create_failure_response('parameter last_date is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('platform_type' in request.GET):
            platform_type = request.GET.get('platform_type')
            if(platform_type not in dict(models.PLATFORM_TYPE).keys()):
                return Response(responses.create_failure_response('platform_type is not a valid date value'), status=status.HTTP_400_BAD_REQUEST)
            objs = objs.filter(platform_type=platform_type)
            # print(objs)
        else:
            return Response(responses.create_failure_response('parameter platform_type is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('city' in request.GET):
            city = request.GET.get('city')
            try:
                city = get_object_or_404(models_country.City, name=city)
            except:
                return Response(responses.create_failure_response('city object not found'), status=status.HTTP_400_BAD_REQUEST)

            objs = objs.filter(city=city)
        else:
            return Response(responses.create_failure_response('parameter city is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        try:
            first_date = datetime.strptime(first_date, "%Y-%m-%d").date()
        except:
            return Response(responses.create_failure_response('first_date is not a valid date value. please provide date string in format YYYY-MM-DD'), status=status.HTTP_400_BAD_REQUEST)

        try:
            last_date = datetime.strptime(last_date, "%Y-%m-%d").date()
        except:
            return Response(responses.create_failure_response('last_date is not a valid date value. please provide date string in format YYYY-MM-DD'), status=status.HTTP_400_BAD_REQUEST)

        max_count = models.MarketingSettings.objects.filter(
            marketing_type="HEADER", platform_type=platform_type, city=city)
        if(max_count.exists()):
            max_count = max_count.first()
            pass
        else:
            max_count = models.MarketingSettings.objects.create(
                marketing_type="HEADER", platform_type=platform_type, city=city, max_count=5)

        dates = []
        # for single_date in daterange(first_date, last_date):
        #     print(single_date.strftime("%Y-%m-%d"))
        delta = timedelta(days=1)
        while first_date <= last_date:
            single_date = first_date
            date = single_date.strftime("%Y-%m-%d")

            headers = objs.filter(
                from_date__lte=single_date,
                to_date__gte=single_date
            )
            # print(headers)

            if(headers.count() > max_count.max_count):    # Only for testing
                # print("max_count exceeded")
                pass

            serializer = serializers.HomepageHeaderMarketingSerializer(
                headers, many=True)

            obj = {
                "date": date,
                "headers": serializer.data,
            }
            dates.append(obj)
            # resp[]
            first_date += delta

        resp = {
            "max_count": max_count.max_count,
            "dates": dates
        }

        return Response(resp)


class SuperAdminHomepageHeaders(APIView):
    # To allow authenticated users only

    def get(self, request):
        objs = models.DefaultHeader.objects.all()

        if('first_date' in request.GET):
            first_date = request.GET.get('first_date')
        else:
            return Response(responses.create_failure_response('parameter first_date is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('last_date' in request.GET):
            last_date = request.GET.get('last_date')
        else:
            return Response(responses.create_failure_response('parameter last_date is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('platform_type' in request.GET):
            platform_type = request.GET.get('platform_type')
            if(platform_type not in dict(models.PLATFORM_TYPE).keys()):
                return Response(responses.create_failure_response('platform_type is not a valid date value'), status=status.HTTP_400_BAD_REQUEST)
            objs = objs.filter(platform_type=platform_type)
            # print(objs)
        else:
            return Response(responses.create_failure_response('parameter platform_type is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('city' in request.GET):
            city = request.GET.get('city')
            try:
                city = get_object_or_404(models_country.City, name=city)
            except:
                return Response(responses.create_failure_response('city object not found'), status=status.HTTP_400_BAD_REQUEST)

            objs = objs.filter(city=city)
        else:
            return Response(responses.create_failure_response('parameter city is not supplied'), status=status.HTTP_400_BAD_REQUEST)


        try:
            first_date = datetime.strptime(first_date, "%Y-%m-%d").date()
        except:
            return Response(responses.create_failure_response('first_date is not a valid date value. please provide date string in format YYYY-MM-DD'), status=status.HTTP_400_BAD_REQUEST)

        try:
            last_date = datetime.strptime(last_date, "%Y-%m-%d").date()
        except:
            return Response(responses.create_failure_response('last_date is not a valid date value. please provide date string in format YYYY-MM-DD'), status=status.HTTP_400_BAD_REQUEST)


        max_count = models.MarketingSettings.objects.filter(
            marketing_type="HEADER", platform_type=platform_type, city=city)
        if(max_count.exists()):
            max_count = max_count.first()
            pass
        else:
            max_count = models.MarketingSettings.objects.create(
                marketing_type="HEADER", platform_type=platform_type, city=city, max_count=5)

        dates = []
        # for single_date in daterange(first_date, last_date):
        delta = timedelta(days=1)
        while first_date <= last_date:
            single_date = first_date
            # print(single_date.strftime("%Y-%m-%d"))
            date = single_date.strftime("%Y-%m-%d")

            headers = objs.filter(
                date=single_date,
            )

            if(headers.count() > max_count.max_count):    # Only for testing
                # print("max_count exceeded")
                pass

            serializer = serializers.SuperAdminHomepageHeaderSerializer(
                headers, many=True, context={'method': 'GET'})

            obj = {
                "date": date,
                "headers": serializer.data,
            }
            dates.append(obj)
            first_date += delta

        resp = {
            "max_count": max_count.max_count,
            "dates": dates
        }

        return Response(resp)


    def post(self, request):
        serializer = serializers.SuperAdminHomepageHeaderSerializer(
            data=request.data, user=request.user)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response()


class SuperAdminHomepageHeader(APIView):
    # To allow authenticated users only
    def delete(self, request, id):
        try:
            obj = models.DefaultHeader.objects.get(id=id)
        except:
            return Response(responses.RESP_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        try:
            obj.delete()
            return Response(responses.create_success_response('object deleted successfully'), status=status.HTTP_204_NO_CONTENT)
        
        except ProtectedError as e:
            return Response(responses.create_failure_response('this object is currently being used. ' + str(e) ) )
        
        except:
            return Response(responses.RESP_INTERNAL_SERVER_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def patch(self, request, id):
        try:
            obj = models.DefaultHeader.objects.get(id=id)
        except:
            return Response(responses.RESP_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        try:
            obj.text = request.data.get("text",obj.text)
            obj.save(update_fields=['text'])
            serializer  = serializers.SuperAdminHomepageHeaderSerializer(obj,user=request.user)
            return Response(serializer.data)
        except:
            return Response(responses.RESP_INTERNAL_SERVER_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
