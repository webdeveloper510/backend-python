from rest_framework import serializers
from django.db.models import Max
from . import models
from superadmin.subapps.countries_and_cities import models as models_country
from superadmin import custom_serializers_fields as csf


class AgeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AgeGroup
        # no, age_group_name, min_age, max_age
        fields = ('id','name','min_age','max_age','country')

        