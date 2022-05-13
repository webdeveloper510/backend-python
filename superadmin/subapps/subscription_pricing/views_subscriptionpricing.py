from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import serializers_subscriptionpricing as serializers
from . import models

from superadmin.subapps.countries_and_cities import serializers as serializers_country
from superadmin.subapps.countries_and_cities import models as models_country

from django.shortcuts import get_object_or_404

# For HTTP Error
from rest_framework import status

# For DRF_csv
from rest_framework.views import APIView
from rest_framework.settings import api_settings
from rest_framework_csv import renderers as r
from common.CustomLimitOffsetPaginator import CustomLimitOffsetPaginator
from authentication import responses


class GetPlansByCountry(APIView):
    # To allow authenticated users only
    permission_classes = (IsAuthenticated,)

    def get(self, request, country_name):
        try:
            country = get_object_or_404(models_country.Country, name=country_name)
        except:
            return Response(responses.RESP_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        pkgs = models.SubscriptionPackage.objects.filter(country=country)

        paginator = CustomLimitOffsetPaginator()
        if(request.GET.get(CustomLimitOffsetPaginator.limit_query_param, False)):
            page = paginator.paginate_queryset(pkgs, request, view=self)
            serializer = serializers.SubscriptionPlanSerializer(
                page, many=True)
            if page is not None:
                return paginator.get_paginated_response(serializer.data)
        else:
            serializer = serializers.SubscriptionPlanSerializer(pkgs, many=True)
            return Response(serializer.data)
        # return Response(serializer.data)


class subscription_types(APIView):
    # To allow authenticated users only
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        resp = dict(models.SUBSCRIPTION_TYPE).keys()
        return Response(resp)



class subscriptionPackage(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        all_packages = models.SubscriptionPackage.objects.all()
        serializer = serializers.SubscriptionPlanSerializer(all_packages, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = serializers.SubscriptionPlanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        


class subscription_package(APIView):
    # To allow authenticated users only
    permission_classes = (IsAuthenticated,)

    def patch(self, request, id):
        try:
            pkg = models.SubscriptionPackage.objects.get(id=id)
        except Exception as e:
            return Response(responses.RESP_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
            
        serializer = serializers.SubscriptionPlanSerializer(
            pkg, data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class SubscriptionPricingRenderer(r.CSVRenderer):
    # header = ['name, price_per_month, price_per_year']
    labels = {
        # 'SubscriptionPricing.no_of_activities': 'no_of_activities',
    }


class GetPlansByCountryCSV(APIView):
    # To allow authenticated users only
    permission_classes = (IsAuthenticated,)
    renderer_classes = (SubscriptionPricingRenderer,) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)

    # renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES)

    def get(self, request, country_name):
        try:
            country = get_object_or_404(models_country.Country, name=country_name)
        except:
            return Response(responses.RESP_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        pkgs = models.SubscriptionPackage.objects.filter(country=country)
        serializer = serializers.SubscriptionPlanSerializer(pkgs, many=True)

        return Response(serializer.data)


