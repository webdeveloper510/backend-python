from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework import serializers as serializers_rf

from . import serializers_marketing as serializers
from . import models
from superadmin.subapps.countries_and_cities import models as models_country

from django.shortcuts import get_object_or_404
from authentication import responses

# For HTTP Error
from rest_framework import status
from datetime import datetime, timedelta

class MarketingSettings(APIView):
    # To allow authenticated users only

    def get(self, request):
        objs = models.MarketingSettings.objects.all()
        if('city' in request.GET):
            city = request.GET.get('city')
            try:
                city = get_object_or_404(models_country.City, name=city)
            except:
                return Response(responses.create_failure_response('city object not found'), status=status.HTTP_400_BAD_REQUEST)

            objs = objs.filter(city=city)
        else:
            return Response(responses.create_failure_response('parameter city is not supplied'), status=status.HTTP_400_BAD_REQUEST)
        response = {}

        marketing_types = ["BANNER", "HEADER"]
        for marketing_type in marketing_types:
            response[marketing_type] = {}
            for platform_type in dict(models.PLATFORM_TYPE).keys():
                entries = objs.filter(marketing_type=marketing_type, platform_type=platform_type)
                if(entries.exists()):
                    max_count = entries.first().max_count
                else:
                    max_count = None
                pass
                response[marketing_type][platform_type] = {"max_count":max_count}
        
        return Response(response)




    def patch(self, request):
        objs = models.MarketingSettings.objects.all()
        if('city' in request.GET):
            city = request.GET.get('city')
            try:
                city = get_object_or_404(models_country.City, name=city)
            except:
                return Response(responses.create_failure_response('city object not found'), status=status.HTTP_400_BAD_REQUEST)

            objs = objs.filter(city=city)
        else:
            return Response(responses.create_failure_response('parameter city is not supplied'), status=status.HTTP_400_BAD_REQUEST)
        
        marketing_types = ["BANNER", "HEADER"]
        
        # print(request.data)
        
        # Update Data
        for marketing_type in marketing_types:
            if(marketing_type in request.data):
                # print('marketing_type present: ', marketing_type)
                for platform_type in dict(models.PLATFORM_TYPE).keys():
                    if(platform_type in request.data[marketing_type]):
                        # print('platform_type present: ', platform_type)
                        if('max_count' in request.data[marketing_type][platform_type] ):
                            entries = objs.filter(marketing_type=marketing_type, platform_type=platform_type)
                            max_count = request.data[marketing_type][platform_type]["max_count"]
                            if(not max_count):
                                raise serializers_rf.ValidationError({"max_count":"invalid max_count value"})
                            if(entries.exists()):
                                entries.update(max_count=max_count )
                                # max_count = entries.first().max_count

                            else:
                                models.MarketingSettings.objects.create(city=city,marketing_type=marketing_type, platform_type=platform_type, max_count=max_count)
                            
        # Build Response
        response = {}
        for marketing_type in marketing_types:
            response[marketing_type] = {}
            for platform_type in dict(models.PLATFORM_TYPE).keys():
                entries = objs.filter(marketing_type=marketing_type, platform_type=platform_type)
                if(entries.exists()):
                    max_count = entries.first().max_count
                else:
                    max_count = None
                pass
                response[marketing_type][platform_type] = {"max_count":max_count}
        
        return Response(response)
        

class MarketingPrice(APIView):
    # To allow authenticated users only

    def get(self, request):
        objs = models.MarketingSettings.objects.all()
        if('city' in request.GET):
            city = request.GET.get('city')
            try:
                city = get_object_or_404(models_country.City, name=city)
            except:
                return Response(responses.create_failure_response('city object not found'), status=status.HTTP_400_BAD_REQUEST)

            objs = objs.filter(city=city)
        else:
            return Response(responses.create_failure_response('parameter city is not supplied'), status=status.HTTP_400_BAD_REQUEST)
        
        
        if('marketing_type' in request.GET):
            marketing_type = request.GET.get('marketing_type')
            print()
            if(marketing_type not in dict(models.MARKETING_TYPE).keys()):
                return Response(responses.create_failure_response('marketing_type is not a valid date value'), status=status.HTTP_400_BAD_REQUEST)
            objs = objs.filter(marketing_type=marketing_type)
            # print(objs)
        else:
            return Response(responses.create_failure_response('parameter marketing_type is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        
        response = {}
        categories = models.Category.objects.values_list("name", flat=True).distinct()
        # print("categories= ", categories)
        for platform_type in dict(models.PLATFORM_TYPE).keys():
            response[platform_type] = []
            for category in categories:
                cat = {"category":category}
                data = models.MarketingPrice.objects.filter(city=city,marketing_type=marketing_type,platform_type=platform_type,category=category)
                if(not data.exists()):
                    obj = models.MarketingPrice.objects.create(city=city,marketing_type=marketing_type,platform_type=platform_type,category=category, days=None,price=None)                    
                    obj = models.MarketingPrice.objects.create(city=city,marketing_type=marketing_type,platform_type=platform_type,category=category, days=1,price=None)                    
                    obj = models.MarketingPrice.objects.create(city=city,marketing_type=marketing_type,platform_type=platform_type,category=category, days=2,price=None)                    
                    data = models.MarketingPrice.objects.filter(city=city,marketing_type=marketing_type,platform_type=platform_type,category=category)
                
                # for entry in data:
                #     if(entry.days):
                #         cat[entry.days] = entry.price
                #     else:
                #         cat["subsequent_days"] = entry.price
                
                sd = data.filter(days=None)
                cat["subsequent_days"] = sd.first().price if sd.exists() else None
                i=1
                while(True):
                    entry = data.filter(days=i)
                    if(entry.exists()):
                        entry = entry.first()
                        cat[entry.days] = entry.price
                    else:
                        break
                    
                    i=i+1

                response[platform_type].append(cat)
        return Response(response)

    def patch(self, request):
        objs = models.MarketingSettings.objects.all()
        if('city' in request.GET):
            city = request.GET.get('city')
            try:
                city = get_object_or_404(models_country.City, name=city)
            except:
                return Response(responses.create_failure_response('city object not found'), status=status.HTTP_400_BAD_REQUEST)

            objs = objs.filter(city=city)
        else:
            return Response(responses.create_failure_response('parameter city is not supplied'), status=status.HTTP_400_BAD_REQUEST)
        
        
        if('marketing_type' in request.GET):
            marketing_type = request.GET.get('marketing_type')
            print()
            if(marketing_type not in dict(models.MARKETING_TYPE).keys()):
                return Response(responses.create_failure_response('marketing_type is not a valid date value'), status=status.HTTP_400_BAD_REQUEST)
            objs = objs.filter(marketing_type=marketing_type)
            # print(objs)
        else:
            return Response(responses.create_failure_response('parameter marketing_type is not supplied'), status=status.HTTP_400_BAD_REQUEST)

        
        categories = models.Category.objects.values_list("name", flat=True).distinct()
        # update fields

        for platform_type in dict(models.PLATFORM_TYPE).keys():
            if(platform_type in request.data):
                for obj in request.data[platform_type]:
                    category = obj['category']
                    if(category in categories):
                        # print("obj = ",  obj)
                        if('subsequent_days' in obj):
                            # print("subsequent_days: ", obj["subsequent_days"])
                            price = obj["subsequent_days"]
                            updated = models.MarketingPrice.objects.filter(city=city,marketing_type=marketing_type,platform_type=platform_type,category=category, days=None).update(price=price)                    
                            # print("updated :", updated)
                        
                        
                        data = models.MarketingPrice.objects.filter(city=city,marketing_type=marketing_type,platform_type=platform_type,category=category)
                        i=1
                        while(True):
                            if( str(i) in obj):
                                entry = data.filter(days=i)
                                if(obj[ str(i)]):
                                    entry.update(price = obj[ str(i)])
                            else:
                                break
                            i=i+1
                        
        # generate response
        response = {}
        for platform_type in dict(models.PLATFORM_TYPE).keys():
            response[platform_type] = []
            for category in categories:
                cat = {"category":category}
                data = models.MarketingPrice.objects.filter(city=city,marketing_type=marketing_type,platform_type=platform_type,category=category)
                if(not data.exists()):
                    obj = models.MarketingPrice.objects.create(city=city,marketing_type=marketing_type,platform_type=platform_type,category=category, days=None,price=None)                    
                    obj = models.MarketingPrice.objects.create(city=city,marketing_type=marketing_type,platform_type=platform_type,category=category, days=1,price=None)                    
                    obj = models.MarketingPrice.objects.create(city=city,marketing_type=marketing_type,platform_type=platform_type,category=category, days=2,price=None)                    
                    data = models.MarketingPrice.objects.filter(city=city,marketing_type=marketing_type,platform_type=platform_type,category=category)
                
                # for entry in data:
                #     if(entry.days):
                #         cat[entry.days] = entry.price
                #     else:
                #         cat["subsequent_days"] = entry.price
                i=1
                while(True):
                    sd = data.filter(days=None)
                    cat["subsequent_days"] = sd.first().price if sd.exists() else None
                    entry = data.filter(days=i)
                    if(entry.exists()):
                        entry = entry.first()
                        cat[entry.days] = entry.price
                    else:
                        break
                    
                    i=i+1

                response[platform_type].append(cat)
        return Response(response)