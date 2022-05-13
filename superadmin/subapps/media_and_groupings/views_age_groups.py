from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

from . import serializers_age_groups as serializers
from . import models
from authentication import decorators as auth_decorators,responses
from superadmin.subapps.countries_and_cities import models as models_country
from common.CustomLimitOffsetPaginator import CustomLimitOffsetPaginator


# For HTTP Error
from rest_framework import status
from django.db.models import ProtectedError


class AgeGroups(ModelViewSet):
    serializer_class=serializers.AgeGroupSerializer
    permission_classes=[IsAuthenticated]
    pagination_class=CustomLimitOffsetPaginator

    def get_queryset(self):
        queryset=models.AgeGroup.objects.all()
        country = self.request.query_params.get('country')
        if country is not None:
            queryset = models.AgeGroup.objects.filter(country__id=country)
        return queryset
