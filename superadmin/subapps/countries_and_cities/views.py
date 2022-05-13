from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authentication import decorators as auth_decorators,responses

from . import models
from . import serializers

from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from . import models
# For HTTP Error
from rest_framework import status

from rest_framework.pagination import LimitOffsetPagination
from common.CustomLimitOffsetPaginator import CustomLimitOffsetPaginator

from rest_framework import generics

from django.utils.decorators import method_decorator
from superadmin import decorators
import csv
from django.db.models import ProtectedError

# =========================================
# List endpoint to Filter for other modules
# =========================================

class countries_list_filters_unsecured(APIView):
    # To allow all users
    def get(self, request):
        Country = models.Country.objects.filter(status="ACTIVE")
        paginator = CustomLimitOffsetPaginator()
        if(request.GET.get(CustomLimitOffsetPaginator.limit_query_param, False)):
            page = paginator.paginate_queryset(Country, request, view=self)
            serializer = serializers.CountryListFilterSerializer(
                page, many=True)
            if page is not None:
                return paginator.get_paginated_response(serializer.data)
        else:
            serializer = serializers.CountryListFilterSerializer(
                Country, many=True)
            return Response(serializer.data)

class city_list_filters_unsecured(APIView):
    # To allow all users
    def get(self, request):
        if("country_id" not in request.GET):
            return Response(responses.create_failure_response('country_id is required parameter'), status=status.HTTP_400_BAD_REQUEST )

        country_id = request.GET["country_id"]
        try:
            country = models.Country.objects.get(id=country_id, status="ACTIVE")
        except:
            return Response(responses.create_failure_response('country doesnot exists'), status=status.HTTP_400_BAD_REQUEST )

        City = models.City.objects.filter(country=country, status="ACTIVE")
        paginator = CustomLimitOffsetPaginator()
        if(request.GET.get(CustomLimitOffsetPaginator.limit_query_param, False)):
            page = paginator.paginate_queryset(City, request, view=self)
            serializer = serializers.CityListFilterSerializer(
                page, many=True)
            if page is not None:
                return paginator.get_paginated_response(serializer.data)
        else:
            serializer = serializers.CityListFilterSerializer(
                City, many=True)
            return Response(serializer.data)

# =========================================

# For Listing countries for User/Vendor registration endpoints
class countries_unsecured(APIView):
    # To allow all users
    def get(self, request):
        Country = models.Country.objects.filter(status="ACTIVE")
        paginator = CustomLimitOffsetPaginator()
        if(request.GET.get(CustomLimitOffsetPaginator.limit_query_param, False)):
            page = paginator.paginate_queryset(Country, request, view=self)
            serializer = serializers.CountrySerializer(
                page, many=True)
            if page is not None:
                return paginator.get_paginated_response(serializer.data)
        else:
            serializer = serializers.CountrySerializer(
                Country, many=True)
            return Response(serializer.data)

class Countries(APIView):

    # @method_decorator(decorators.log_db_read_operation)
    def get(self, request):
        Serializer = serializers.CountrySerializer
        if('mode' in request.GET):
            mode = request.GET["mode"]
            if(mode.lower() == "compact"):
                Serializer = serializers.CountryCompactSerializer
        
        Country = models.Country.objects.filter(status="ACTIVE")
        paginator = CustomLimitOffsetPaginator()
        if(request.GET.get(CustomLimitOffsetPaginator.limit_query_param, False)):
            page = paginator.paginate_queryset(Country, request, view=self)
            serializer = Serializer(
                page, many=True)
            if page is not None:
                return paginator.get_paginated_response(serializer.data)
        else:
            serializer = Serializer(
                Country, many=True)
            return Response(serializer.data)
    
    # @method_decorator(decorators.log_db_create_operation)
    def post(self, request):
        serializer = serializers.CountrySerializer(data=request.data)
        if(serializer.is_valid()):
            obj = serializer.save()
            try:
                obj.status = "ACTIVE"
                obj.save()
            except:
                return Response( responses.RESP_INTERNAL_SERVER_ERROR , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CountriesCSV(APIView):
    # To allow authenticated users only
    @method_decorator(decorators.log_db_read_operation)
    def get(self, request):
        # model = models.Family
        objs = models.Country.objects.filter(status="ACTIVE")
        # objs = models.Family.objects.all()
        response = HttpResponse(content_type='text/csv')
        # force download
        file_name = "Countries.csv"
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(file_name)
        # the csv writer
        writer = csv.writer(response)

        titles = ['name','abbr', 'cities','city status','currency', 'status']


        writer.writerow(titles)

        for obj in objs:    
            writer.writerow([obj.name,obj.abbr,'', '', obj.currency if models.Currency.objects.filter(country=obj) else None,obj.status])
            for city in obj.cities.all():
                writer.writerow(['','',city.name,city.status,"", "" ])


        return response

class Country(APIView):
    # To allow authenticated users only

    # @method_decorator(decorators.log_db_delete_operation)
    def get(self, request, id):
        try:
            obj = models.Country.objects.get(id=id, status="ACTIVE")
        except:
            return Response(responses.RESP_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.CountrySerializer(obj)
        return Response(serializer.data)


    # @method_decorator(decorators.log_db_delete_operation)
    def delete(self, request, id):
        try:
            obj = models.Country.objects.get(id=id, status="ACTIVE")
        except:
            return Response(responses.RESP_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        
        try:
            
            obj.delete()
            return Response(responses.create_success_response('object deleted successfully'), status=status.HTTP_204_NO_CONTENT)
        
        except ProtectedError as e:
            return Response(responses.create_failure_response('this object is currently being used. ' + str(e) ), status=status.HTTP_400_BAD_REQUEST )
        
        except:
            # return Response(responses.RESP_INTERNAL_SERVER_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(responses.create_failure_response("Country is actively being used. can't delete it."), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # @method_decorator(decorators.log_db_update_operation)
    def patch(self, request, id):
        try:
            # obj = models.Country.objects.get(id=id, status="ACTIVE")
            obj = models.Country.objects.get(id=id)
        except Exception as e:
            return Response(responses.RESP_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.CountrySerializer(obj, data=request.data, partial=True)
        if(serializer.is_valid()):
            serializer.save()
            try:
                pass
            except:
                return Response(responses.RESP_INTERNAL_SERVER_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# =============================================================

class Cities(APIView):
    # To allow authenticated users only

    def get(self, request, cid,action):
        Serializer = serializers.CitySerializer
        if('mode' in request.GET):
            mode = request.GET["mode"]
            if(mode.lower() == "compact"):
                Serializer = serializers.CityCompactSerializer

        cities = models.City.objects.filter(country__id=cid)
        paginator = CustomLimitOffsetPaginator()
        if(request.GET.get(CustomLimitOffsetPaginator.limit_query_param, False)):
            page = paginator.paginate_queryset(cities, request, view=self)
            serializer = Serializer(page, many=True)
            if page is not None:
                return paginator.get_paginated_response(serializer.data)
        else:
            serializer = Serializer(cities, many=True)
            return Response(serializer.data)
    
    
    def post(self, request, cid,action):
        if action == 'create': 
            try:
                country = models.Country.objects.get(id = cid)
            except:
                return Response(responses.RESP_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
            
            serializer = serializers.CitySerializer(data=request.data)
            if(serializer.is_valid()):
                obj = serializer.save(country = country)
                # obj.created_by = request.user
                # obj.country = country
                # obj.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if action == 'delete':
            try:
                country = models.Country.objects.get(id = cid)
            except:
                return Response(responses.create_failure_response('country does not exists'), status=status.HTTP_404_NOT_FOUND)
            try:
                id_list = request.data['id_list']
                pass
            except:
                return Response(responses.create_failure_response('parameter id_list not provided') , status=status.HTTP_400_BAD_REQUEST)
            
            succ_list = []
            failed_list = []
            error_messages = []
            try:
                for id in id_list:
                    try:
                        obj = models.City.objects.get(id=id,country__id=cid).delete()
                        succ_list.append(id)
                    
                    except ProtectedError as e:
                        error_messages.append( 'This object with id ' + str(id) + ' is currently being used. ' + str(e) )
                        failed_list.append(id)
                        # return Response(responses.create_failure_response('this object with id ' + str(id) + ' is currently being used. ' + str(e) ) )
            
                    except:
                        error_messages.append( 'This object with id ' + str(id) + ' does not exists')
                        failed_list.append(id)
            except:
                return Response(responses.create_failure_response('parameter id_list must be a non empty list') , status=status.HTTP_400_BAD_REQUEST)

            return Response({"success_list":succ_list, "failed_list": failed_list, "error_messages":error_messages}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error":"Invalid Action. Valid actions are create,delete"},status=status.HTTP_400_BAD_REQUEST)

class City(APIView):
    # To allow authenticated users only
    permission_classes = (IsAuthenticated,)

    def delete(self, request,cid, id):
        try:
            obj = models.City.objects.get(id=id)
        except:
            return Response(responses.RESP_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        
        try:
            obj.delete()
            pass
            return Response(responses.create_success_response('object deleted successfully'))
        
        except ProtectedError as e:
            return Response(responses.create_failure_response('this object is currently being used. ' + str(e) ) )
        
        except:
            return Response(responses.RESP_INTERNAL_SERVER_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

    def patch(self, request,cid, id):
        try:
            obj = models.City.objects.get(id=id)
            pass
        except:
            return Response(responses.RESP_NOT_FOUND , status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.CitySerializer(obj, data=request.data, partial=True)
        if(serializer.is_valid()):
            obj = serializer.save()
            obj.updated_by = request.user
            obj.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==================================================
# ==================================================

class Regions(APIView):
    # To allow authenticated users only

    def get(self, request, country, city,action):
        if(not models.Country.objects.filter(id=country).exists() ):
            return Response(responses.create_failure_response('country does not exists'), status=status.HTTP_404_NOT_FOUND)
        if(not models.City.objects.filter(id=city, country__id=country).exists() ):
            return Response(responses.create_failure_response('city does not exists'), status=status.HTTP_404_NOT_FOUND)

        Serializer = serializers.RegionSerializer
        if('mode' in request.GET):
            mode = request.GET["mode"]
            if(mode.lower() == "compact"):
                Serializer = serializers.RegionCompactSerializer

        regions = models.Region.objects.filter(city__country__id=country, city__id=city)
        paginator = CustomLimitOffsetPaginator()
        if(request.GET.get(CustomLimitOffsetPaginator.limit_query_param, False)):
            page = paginator.paginate_queryset(regions, request, view=self)
            serializer = Serializer(
                page, many=True)
            if page is not None:
                return paginator.get_paginated_response(serializer.data)
        else:
            serializer = Serializer(
                regions, many=True)
            return Response(serializer.data)
    

    def post(self, request, country, city,action):
        if action == 'create':
            if(not models.Country.objects.filter(id=country).exists() ):
                return Response(responses.create_failure_response('country does not exists'), status=status.HTTP_404_NOT_FOUND)
            if(not models.City.objects.filter(id=city, country__id=country).exists() ):
                return Response(responses.create_failure_response('city does not exists'), status=status.HTTP_404_NOT_FOUND)
            city = models.City.objects.get(id=city, country__id=country)
            serializer = serializers.RegionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(city=city)
            return Response(serializer.data)
        if action == 'delete':
            if(not models.Country.objects.filter(id=country).exists() ):
                return Response(responses.create_failure_response('country does not exists'), status=status.HTTP_404_NOT_FOUND)
            if(not models.City.objects.filter(id=city, country__id=country).exists() ):
                return Response(responses.create_failure_response('city does not exists'), status=status.HTTP_404_NOT_FOUND)

            try:
                id_list = request.data['id_list']
                
            except:
                return Response(responses.create_failure_response('parameter id_list not provided') , status=status.HTTP_400_BAD_REQUEST)
            if not (isinstance(id_list, list)):
                return Response(responses.create_failure_response("parameter id_list must be a list"), status=status.HTTP_400_BAD_REQUEST)

            succ_list = []
            failed_list = []
            error_messages = []
            try:
                for id in id_list:
                    try:
                        models.Region.objects.get(id=id,city__id=city).delete()
                        succ_list.append(id)
                    
                    except ProtectedError as e:
                        error_messages.append( 'this object with id ' + str(id) + ' is currently being used. ' + str(e) )
                        failed_list.append(id)
                        # return Response(responses.create_failure_response('this object with id ' + str(id) + ' is currently being used. ' + str(e) ) )
            
                    except:
                        error_messages.append( 'object with id ' + str(id) + ' does not exists:')
                        failed_list.append(id)
            except:
                return Response(responses.create_failure_response('parameter id_list must be a non empty list') , status=status.HTTP_400_BAD_REQUEST)

            return Response({"success_list":succ_list, "failed_list": failed_list, "error_messages":error_messages}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error":"Invalid Action. Valid actions are create,delete"},status=status.HTTP_400_BAD_REQUEST)



        
    

class Areas(APIView):
    # To allow authenticated users only

    def get(self, request, country, city, region,action):
        if action == 'list':
            if(not models.Country.objects.filter(id=country).exists() ):
                return Response(responses.create_failure_response('country does not exists'), status=status.HTTP_404_NOT_FOUND)
            if(not models.City.objects.filter(id=city, country__id=country).exists() ):
                return Response(responses.create_failure_response('city does not exists'), status=status.HTTP_404_NOT_FOUND)
            if(not models.Region.objects.filter(id=region, city__id=city, city__country__id=country).exists() ):
                return Response(responses.create_failure_response('region does not exists'), status=status.HTTP_404_NOT_FOUND)

            Serializer = serializers.AreaSerializer
            # if('mode' in request.GET):
            #     mode = request.GET["mode"]
            #     if(mode.lower() == "compact"):
            #         Serializer = serializers.RegionCompactSerializer

            areas = models.Area.objects.filter(region__id=region, region__city__country__id=country, region__city__id=city)

            paginator = CustomLimitOffsetPaginator()
            if(request.GET.get(CustomLimitOffsetPaginator.limit_query_param, False)):
                page = paginator.paginate_queryset(areas, request, view=self)
                serializer = Serializer(
                    page, many=True)
                if page is not None:
                    return paginator.get_paginated_response(serializer.data)
            else:
                serializer = Serializer(
                    areas, many=True)
                return Response(serializer.data)
        else:
            return Response({"error":"Invalid Action. Valid action is list"},status=status.HTTP_400_BAD_REQUEST)


    def post(self,request,country, city, region,action):
        if action == "delete":
            if(not models.Country.objects.filter(id=country).exists() ):
                return Response(responses.create_failure_response('country does not exists'), status=status.HTTP_404_NOT_FOUND)
            if(not models.City.objects.filter(id=city, country__id=country).exists() ):
                return Response(responses.create_failure_response('city does not exists'), status=status.HTTP_404_NOT_FOUND)
            if(not models.Region.objects.filter(id=region, city__id=city).exists() ):
                return Response(responses.create_failure_response('region does not exists'), status=status.HTTP_404_NOT_FOUND)

            try:
                id_list = request.data['id_list']
                pass
            except:
                return Response(responses.create_failure_response('parameter id_list not provided') , status=status.HTTP_400_BAD_REQUEST)
            # if 'id_list' type is not list type then give error
            if not (isinstance(id_list, list)):
                return Response(responses.create_failure_response("parameter id_list must be a list"), status=status.HTTP_400_BAD_REQUEST)


            succ_list = []
            failed_list = []
            error_messages = []
            try:
                for id in id_list:
                    try:
                        obj = models.Area.objects.get(id=id,region__id=region).delete()
                        succ_list.append(id)
                    
                    except ProtectedError as e:
                        error_messages.append( 'this object with id ' + str(id) + ' is currently being used. ' + str(e) )
                        failed_list.append(id)
                        # return Response(responses.create_failure_response('this object with id ' + str(id) + ' is currently being used. ' + str(e) ) )
            
                    except:
                        error_messages.append( 'object with id ' + str(id) + ' does not exists:')
                        failed_list.append(id)
            except:
                return Response(responses.create_failure_response('parameter id_list must be a non empty list') , status=status.HTTP_400_BAD_REQUEST)

            return Response({"success_list":succ_list, "failed_list": failed_list, "error_messages":error_messages}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error":"Invalid Action. Valid action is delete"},status=status.HTTP_400_BAD_REQUEST)
             
