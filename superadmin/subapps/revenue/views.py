from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import models
from superadmin.subapps.countries_and_cities import models as models_country
from superadmin.subapps.media_and_groupings import models as models_media

from django.shortcuts import get_object_or_404

# For HTTP Error
from rest_framework import status
from datetime import datetime, time, timedelta

from django.db.models import ProtectedError

from superadmin.subapps.subscription_pricing import models as models_subscription
from rest_framework.settings import api_settings
from rest_framework_csv import renderers as r
from authentication import responses

from . import methods


# =======================
#       Methods
# =======================


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
# =======================

class SubscriptionRevenue(APIView):
    # To allow authenticated users only

    def get(self, request):
        objs = models_subscription.VendorSubscription.objects.all().exclude(status="SENT")
        first_date = None
        last_date = None
        if ('day' in request.GET):
            days = request.GET['day']
            if(days == 'last_thirty_day'):
                last_date = datetime.today()
                first_date = last_date - timedelta(days=30)
                last_date = last_date.date()
                first_date = first_date.date()

            elif (days == 'last_sixty_day'):
                last_date = datetime.today()
                first_date = last_date - timedelta(days=60)
                last_date = last_date.date()
                first_date = first_date.date()
            else: 
                return Response(responses.create_failure_response("parameter 'day' is not valid value. valid options are last_thirty_day/last_sixty_day"), status=status.HTTP_400_BAD_REQUEST)

        if('first_date' in request.GET) or ('last_date' in request.GET):
            if('first_date' in request.GET):
                first_date = request.GET.get('first_date')
            else:
                return Response(responses.create_failure_response('parameter first_date is not supplied'), status=status.HTTP_400_BAD_REQUEST)

            if('last_date' in request.GET):
                last_date = request.GET.get('last_date')
            else:
                return Response(responses.create_failure_response('parameter last_date is not supplied'), status=status.HTTP_400_BAD_REQUEST)
            
            try:
                first_date = datetime.strptime(first_date, "%Y-%m-%d").date()
            except:
                return Response(responses.create_failure_response('first_date is not a valid date value. please provide date string in format YYYY-MM-DD'), status=status.HTTP_400_BAD_REQUEST)

            try:
                last_date = datetime.strptime(last_date, "%Y-%m-%d").date()
            except:
                return Response(responses.create_failure_response('last_date is not a valid date value. please provide date string in format YYYY-MM-DD'), status=status.HTTP_400_BAD_REQUEST)



        if('type' in request.GET):
            type = request.GET.get('type')
            if(type not in ["TIME_BASED", "ACCOUNTING"]):
                return Response(responses.create_failure_response('revenue type is not a valid value. It can have values TIME_BASED or ACCOUNTING'), status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response(responses.create_failure_response('parameter type is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('country' in request.GET):
            country = request.GET.get('country')
            try:
                country = get_object_or_404(models_country.Country, name=country)
            except:
                return Response(responses.create_failure_response('country object not found'), status=status.HTTP_400_BAD_REQUEST)

            objs = objs.filter(vendor__country=country)
            # print(objs)
        else:
            return Response(responses.create_failure_response('parameter country is not supplied'), status=status.HTTP_400_BAD_REQUEST)
        city=None
        if('city' in request.GET):
            city = request.GET.get('city')
            try:
                city = get_object_or_404(models_country.City, name=city)
            except:
                return Response(responses.create_failure_response('city object not found'), status=status.HTTP_400_BAD_REQUEST)

            objs = objs.filter(vendor__country=country, vendor__city=city)
        # else:
        #     return Response(responses.create_failure_response('parameter city is not supplied'), status=status.HTTP_400_BAD_REQUEST)
        # print(objs)

        # if first_date and last_date:
        #     # start_date 
        #     objs= objs.filter(start_date__gte=first_date)

        resp_objs = methods.compute_subscription_revenue(type, objs, first_date, last_date, city, country.name)

       
        return Response(resp_objs)





class SubscriptionRevenueRenderer (r.CSVRenderer):
    header = ['subscription_type', 'net_revenue', 'tax', 
    'gross_revenue', 'number_of_subscriptions', 'average_subscription'
    ]
    labels = {}

class SubscriptionRevenueCSV(APIView):
    # To allow authenticated users only
    permission_classes = (IsAuthenticated,)
    renderer_classes = (SubscriptionRevenueRenderer, ) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)

    def get(self, request):
        objs = models_subscription.VendorSubscription.objects.all().exclude(status="SENT")

        if('first_date' in request.GET):
            first_date = request.GET.get('first_date')
        else:
            return Response(responses.create_failure_response('parameter first_date is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('last_date' in request.GET):
            last_date = request.GET.get('last_date')
        else:
            return Response(responses.create_failure_response('parameter last_date is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('type' in request.GET):
            type = request.GET.get('type')
            print()
            if(type not in ["TIME_BASED", "ACCOUNTING"]):
                return Response(responses.create_failure_response('revenue type is not a valid value. It can have values TIME_BASED or ACCOUNTING'), status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response(responses.create_failure_response('parameter type is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('country' in request.GET):
            country = request.GET.get('country')
            try:
                country = get_object_or_404(models_country.Country, name=country)
            except:
                return Response(responses.create_failure_response('country object not found'), status=status.HTTP_400_BAD_REQUEST)

            objs = objs.filter(vendor__country=country)
        else:
            return Response(responses.create_failure_response('parameter country is not supplied'), status=status.HTTP_400_BAD_REQUEST)
        
        if('city' in request.GET):
            city = request.GET.get('city')
            try:
                city = get_object_or_404(models_country.City, name=city)
            except:
                return Response(responses.create_failure_response('city object not found'), status=status.HTTP_400_BAD_REQUEST)

            objs = objs.filter(vendor__country=country, vendor__city=city)
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

        resp_objs = methods.compute_subscription_revenue(type, objs, first_date, last_date)

        return Response(resp_objs)

# ====================================================
#                 Advertising Revenue
# ====================================================



class AdvertisingRevenueSummary(APIView):
    # To allow authenticated users only

    def get(self, request):
        objs = models_media.Marketing.objects.all().order_by('from_date')
        first_date = None
        last_date = None
        if ('day' in request.GET):
            days = request.GET['day']
            if(days == 'last_thirty_day'):
                last_date = datetime.today()
                first_date = last_date - timedelta(days=30)
                last_date = last_date.date()
                first_date = first_date.date()
            elif (days == 'last_sixty_day'):
                last_date = datetime.today()
                first_date = last_date - timedelta(days=60)
                last_date = last_date.date()
                first_date = first_date.date()
            else: 
                return Response(responses.create_failure_response("parameter 'day' is not valid value. valid options are last_thirty_day/last_sixty_day"), status=status.HTTP_400_BAD_REQUEST)

        if('first_date' in request.GET) or ('last_date' in request.GET):
            if('first_date' in request.GET):
                first_date = request.GET.get('first_date')
            else:
                return Response(responses.create_failure_response('parameter first_date is not supplied'), status=status.HTTP_400_BAD_REQUEST)

            if('last_date' in request.GET):
                last_date = request.GET.get('last_date')
            else:
                return Response(responses.create_failure_response('parameter last_date is not supplied'), status=status.HTTP_400_BAD_REQUEST)
            
            try:
                first_date = datetime.strptime(first_date, "%Y-%m-%d").date()
            except:
                return Response(responses.create_failure_response('first_date is not a valid date value. please provide date string in format YYYY-MM-DD'), status=status.HTTP_400_BAD_REQUEST)

            try:
                last_date = datetime.strptime(last_date, "%Y-%m-%d").date()
            except:
                return Response(responses.create_failure_response('last_date is not a valid date value. please provide date string in format YYYY-MM-DD'), status=status.HTTP_400_BAD_REQUEST)


        if('type' in request.GET):
            type = request.GET.get('type')
            print()
            if(type not in ["TIME_BASED", "ACCOUNTING"]):
                return Response(responses.create_failure_response('revenue type is not a valid value. It can have values TIME_BASED or ACCOUNTING'), status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response(responses.create_failure_response('parameter type is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('country' in request.GET):
            country = request.GET.get('country')
            try:
                country = get_object_or_404(models_country.Country, name=country)
            except:
                return Response(responses.create_failure_response('country object not found'), status=status.HTTP_400_BAD_REQUEST)

            # objs = objs.filter(vendor__country=country)
        else:
            return Response(responses.create_failure_response('parameter country is not supplied'), status=status.HTTP_400_BAD_REQUEST)
        
        if('city' in request.GET):
            city = request.GET.get('city')
            try:
                city = get_object_or_404(models_country.City, name=city, country=country)
            except:
                return Response(responses.create_failure_response('city object not found'), status=status.HTTP_400_BAD_REQUEST)

            objs = objs.filter(city=city)
        # else:
        #     return Response(responses.create_failure_response('parameter city is not supplied'), status=status.HTTP_400_BAD_REQUEST)


        
        resp_objs = methods.compute_advertising_revenue(type, objs, first_date, last_date)

        
        return Response(resp_objs)



class AdvertisingRevenueSummaryRenderer (r.CSVRenderer):
    header = ['ad_type', 'net_revenue', 'tax', 
    'gross_revenue', 'number_of_subscriptions', 'average_subscription'
    ]
    labels = {}

class AdvertisingRevenueSummaryCSV(APIView):
    # To allow authenticated users only
    permission_classes = (IsAuthenticated,)
    renderer_classes = (AdvertisingRevenueSummaryRenderer, ) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)

    def get(self, request):
        objs = models_media.Marketing.objects.all()

        if('first_date' in request.GET):
            first_date = request.GET.get('first_date')
        else:
            return Response(responses.create_failure_response('parameter first_date is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('last_date' in request.GET):
            last_date = request.GET.get('last_date')
        else:
            return Response(responses.create_failure_response('parameter last_date is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('type' in request.GET):
            type = request.GET.get('type')
            print()
            if(type not in ["TIME_BASED", "ACCOUNTING"]):
                return Response(responses.create_failure_response('revenue type is not a valid value. It can have values TIME_BASED or ACCOUNTING'), status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response(responses.create_failure_response('parameter type is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('country' in request.GET):
            country = request.GET.get('country')
            try:
                country = get_object_or_404(models_country.Country, name=country)
            except:
                return Response(responses.create_failure_response('country object not found'), status=status.HTTP_400_BAD_REQUEST)

            # objs = objs.filter(vendor__country=country)
        else:
            return Response(responses.create_failure_response('parameter country is not supplied'), status=status.HTTP_400_BAD_REQUEST)
        
        if('city' in request.GET):
            city = request.GET.get('city')
            try:
                city = get_object_or_404(models_country.City, name=city, country=country)
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

        resp_objs = methods.compute_advertising_revenue(type, objs, first_date, last_date)

        
        return Response(resp_objs)



class BannerAdvertisingRevenue(APIView):
    # To allow authenticated users only

    def get(self, request):
        objs = models_media.Marketing.objects.filter(type="BANNER").exclude(status="SENT")
        first_date = None
        last_date = None
        if ('day' in request.GET):
            days = request.GET['day']

            if(days == 'last_thirty_day'):
                last_date = datetime.today()
                first_date = last_date - timedelta(days=30)
                last_date = last_date.date()
                first_date = first_date.date()

            elif (days == 'last_sixty_day'):
                last_date = datetime.today()
                first_date = last_date - timedelta(days=60)
                last_date = last_date.date()
                first_date = first_date.date()
            else: 
                return Response(responses.create_failure_response('parameter day is not valid. valid options are last_thirty_day/last_sixty_day'), status=status.HTTP_400_BAD_REQUEST)

            

        if('first_date' in request.GET) or ('last_date' in request.GET):
            if('first_date' in request.GET):
                first_date = request.GET.get('first_date')
            else:
                return Response(responses.create_failure_response('parameter first_date is not supplied'), status=status.HTTP_400_BAD_REQUEST)

            if('last_date' in request.GET):
                last_date = request.GET.get('last_date')
            else:
                return Response(responses.create_failure_response('parameter last_date is not supplied'), status=status.HTTP_400_BAD_REQUEST)


            try:
                first_date = datetime.strptime(first_date, "%Y-%m-%d").date()
            except:
                return Response(responses.create_failure_response('first_date is not a valid date value. please provide date string in format YYYY-MM-DD'), status=status.HTTP_400_BAD_REQUEST)

            try:
                last_date = datetime.strptime(last_date, "%Y-%m-%d").date()
            except:
                return Response(responses.create_failure_response('last_date is not a valid date value. please provide date string in format YYYY-MM-DD'), status=status.HTTP_400_BAD_REQUEST)

        if('type' in request.GET):
            type = request.GET.get('type')
            print()
            if(type not in ["TIME_BASED", "ACCOUNTING"]):
                return Response(responses.create_failure_response('revenue type is not a valid value. It can have values TIME_BASED or ACCOUNTING'), status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response(responses.create_failure_response('parameter type is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('country' in request.GET):
            country = request.GET.get('country')
            try:
                country = get_object_or_404(models_country.Country, name=country)
            except:
                return Response(responses.create_failure_response('country object not found'), status=status.HTTP_400_BAD_REQUEST)

            # objs = objs.filter(vendor__country=country)
        else:
            return Response(responses.create_failure_response('parameter country is not supplied'), status=status.HTTP_400_BAD_REQUEST)
        
        if('city' in request.GET):
            city = request.GET.get('city')
            try:
                city = get_object_or_404(models_country.City, name=city, country=country)
            except:
                return Response(responses.create_failure_response('city object not found'), status=status.HTTP_400_BAD_REQUEST)

            objs = objs.filter(city=city)
        # else:
        #     return Response(responses.create_failure_response('parameter city is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        resp_objs = methods.compute_banner_marketing_revenue(type, objs, first_date, last_date)

        
        return Response(resp_objs)



class BannerAdvertisingRevenueRenderer (r.CSVRenderer):
    header = ['category', 'net_revenue', 'tax', 
    'gross_revenue', 'number_of_subscriptions', 'average_subscription'
    ]
    labels = {}

class BannerAdvertisingRevenueCSV(APIView):
    # To allow authenticated users only
    permission_classes = (IsAuthenticated,)
    renderer_classes = (BannerAdvertisingRevenueRenderer, ) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)
    

    def get(self, request):
        objs = models_media.Marketing.objects.filter(type="BANNER").exclude(status="SENT")

        if('first_date' in request.GET):
            first_date = request.GET.get('first_date')
        else:
            return Response(responses.create_failure_response('parameter first_date is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('last_date' in request.GET):
            last_date = request.GET.get('last_date')
        else:
            return Response(responses.create_failure_response('parameter last_date is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('type' in request.GET):
            type = request.GET.get('type')
            print()
            if(type not in ["TIME_BASED", "ACCOUNTING"]):
                return Response(responses.create_failure_response('revenue type is not a valid value. It can have values TIME_BASED or ACCOUNTING'), status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response(responses.create_failure_response('parameter type is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('country' in request.GET):
            country = request.GET.get('country')
            try:
                country = get_object_or_404(models_country.Country, name=country)
            except:
                return Response(responses.create_failure_response('country object not found'), status=status.HTTP_400_BAD_REQUEST)

            # objs = objs.filter(vendor__country=country)
        else:
            return Response(responses.create_failure_response('parameter country is not supplied'), status=status.HTTP_400_BAD_REQUEST)
        
        if('city' in request.GET):
            city = request.GET.get('city')
            try:
                city = get_object_or_404(models_country.City, name=city, country=country)
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

        resp_objs = methods.compute_banner_marketing_revenue(type, objs, first_date, last_date)

        
        return Response(resp_objs)



class SearchWordsAdvertisingRevenue(APIView):
    # To allow authenticated users only
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        objs = models_media.Marketing.objects.filter(type="SEARCH_WORDS")
        first_date = None
        last_date = None
        if ('day' in request.GET):
            days = request.GET['day']

            if(days == 'last_thirty_day'):
                last_date = datetime.today()
                first_date = last_date - timedelta(days=30)
                last_date = last_date.date()
                first_date = first_date.date()

            elif (days == 'last_sixty_day'):
                last_date = datetime.today()
                first_date = last_date - timedelta(days=60)
                last_date = last_date.date()
                first_date = first_date.date()
            else: 
                return Response(responses.create_failure_response('parameter day is not valid. valid options are last_thirty_day/last_sixty_day'), status=status.HTTP_400_BAD_REQUEST)


        if('first_date' in request.GET) or  ('last_date' in request.GET):
            if('first_date' in request.GET):
                first_date = request.GET.get('first_date')
            else:
                return Response(responses.create_failure_response('parameter first_date is not supplied'), status=status.HTTP_400_BAD_REQUEST)

            if('last_date' in request.GET):
                last_date = request.GET.get('last_date')
            else:
                return Response(responses.create_failure_response('parameter last_date is not supplied'), status=status.HTTP_400_BAD_REQUEST)
            
            try:
                first_date = datetime.strptime(first_date, "%Y-%m-%d").date()
            except:
                return Response(responses.create_failure_response('first_date is not a valid date value. please provide date string in format YYYY-MM-DD'), status=status.HTTP_400_BAD_REQUEST)

            try:
                last_date = datetime.strptime(last_date, "%Y-%m-%d").date()
            except:
                return Response(responses.create_failure_response('last_date is not a valid date value. please provide date string in format YYYY-MM-DD'), status=status.HTTP_400_BAD_REQUEST)



        if('type' in request.GET):
            type = request.GET.get('type')
            if(type not in ["TIME_BASED", "ACCOUNTING"]):
                return Response(responses.create_failure_response('revenue type is not a valid value. It can have values TIME_BASED or ACCOUNTING'), status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response(responses.create_failure_response('parameter type is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('country' in request.GET):
            country = request.GET.get('country')
            try:
                country = get_object_or_404(models_country.Country, name=country)
            except:
                return Response(responses.create_failure_response('country object not found'), status=status.HTTP_400_BAD_REQUEST)

            # objs = objs.filter(vendor__country=country)
        else:
            return Response(responses.create_failure_response('parameter country is not supplied'), status=status.HTTP_400_BAD_REQUEST)
        
        if('city' in request.GET):
            city = request.GET.get('city')
            try:
                city = get_object_or_404(models_country.City, name=city, country=country)
            except:
                return Response(responses.create_failure_response('city object not found'), status=status.HTTP_400_BAD_REQUEST)

            objs = objs.filter(city=city)
        # else:
        #     return Response(responses.create_failure_response('parameter city is not supplied'), status=status.HTTP_400_BAD_REQUEST)


        resp_objs = methods.compute_search_word_marketing_revenue(type, objs, first_date, last_date)

        
        return Response(resp_objs)


class SearchWordsAdvertisingRevenueRenderer (r.CSVRenderer):
    header = ['word_count', 'net_revenue', 'tax', 
    'gross_revenue', 'number_of_subscriptions', 'average_subscription'
    ]
    labels = {}

class SearchWordsAdvertisingRevenueCSV(APIView):
    # To allow authenticated users only
    permission_classes = (IsAuthenticated,)
    renderer_classes = (SearchWordsAdvertisingRevenueRenderer, ) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)

    def get(self, request):
        objs = models_media.Marketing.objects.filter(type="SEARCH_WORDS")
        # print("initial objs =",objs)

        if('first_date' in request.GET):
            first_date = request.GET.get('first_date')
        else:
            return Response(responses.create_failure_response('parameter first_date is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('last_date' in request.GET):
            last_date = request.GET.get('last_date')
        else:
            return Response(responses.create_failure_response('parameter last_date is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('type' in request.GET):
            type = request.GET.get('type')
            print()
            if(type not in ["TIME_BASED", "ACCOUNTING"]):
                return Response(responses.create_failure_response('revenue type is not a valid value. It can have values TIME_BASED or ACCOUNTING'), status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response(responses.create_failure_response('parameter type is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        if('country' in request.GET):
            country = request.GET.get('country')
            try:
                country = get_object_or_404(models_country.Country, name=country)
            except:
                return Response(responses.create_failure_response('country object not found'), status=status.HTTP_400_BAD_REQUEST)

            # objs = objs.filter(vendor__country=country)
        else:
            return Response(responses.create_failure_response('parameter country is not supplied'), status=status.HTTP_400_BAD_REQUEST)
        
        if('city' in request.GET):
            city = request.GET.get('city')
            try:
                city = get_object_or_404(models_country.City, name=city, country=country)
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

        print("final objs =",objs)

        resp_objs = methods.compute_search_word_marketing_revenue(type, objs, first_date, last_date)

        
        return Response(resp_objs)
