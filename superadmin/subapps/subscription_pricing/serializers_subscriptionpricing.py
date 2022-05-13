from os import name
from superadmin.subapps.countries_and_cities.models import Country
from django.db import transaction
from rest_framework import serializers
# from rest_framework.fields import WritableField
from . import models
from superadmin import custom_serializers_fields as csf

# ===================================================================
''' Custom Serializer Method field to add read write support to SerializerMethodField '''
# ===================================================================


class ReadWriteSerializerMethodField(serializers.SerializerMethodField):
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs['source'] = '*'
        super(serializers.SerializerMethodField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return {self.field_name: data}
# ===================================================================

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubscriptionPackage
        fields = '__all__'


class SubscriptionPlanForVendorSubscription(serializers.ModelSerializer):
    class Meta:
        model=models.SubscriptionPackage
        fields = (
            'subscription_type',
            'no_of_locations',
            'no_of_subadmins',
            'no_of_media',
            'has_trial_class',
            'has_promotions',
            'has_reports',
            'has_dashboard',
            'has_term_renewal',
            'baner_credit',
            'header_credit',
            'search_word_credit',
            'price_per_month',
        )
