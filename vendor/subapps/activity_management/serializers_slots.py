# import random
# import string

from rest_framework import serializers
from . import models, methods
# from itertools import groupby
# from operator import itemgetter
import json
from superadmin.subapps.media_and_groupings.models import AgeGroup as agegroupmodel
# from superadmin.subapps.media_and_groupings.models import Attribute as attributemodel
# from superadmin.subapps.media_and_groupings.serializers_attributes import AttributeSerializer
from superadmin import custom_serializers_fields as csf

from vendor.subapps.profile import models as models_profile

class SlotSerializer(serializers.ModelSerializer):
    slotdate = serializers.DateField(format="%d-%m-%Y", input_formats=['%d-%m-%Y',])
    publishdate = serializers.DateField(format="%d-%m-%Y", input_formats=['%d-%m-%Y',], allow_null=True)
    class Meta:
        model = models.Slot
        fields = ('id','slotdate','publishdate', 'totalenrolled', 'totalavailableslots','activity','location','price',
                  'tier1pricing','tier2pricing','tier3pricing')
        # read_only_fields = ('totalenrolled',)
        extra_kwargs = {
            'activity': {'write_only': True},
            'location': {'write_only': True},
        }
    def create(self, validated_data):
        if (models.Slot.objects.filter(slotdate=validated_data.get('slotdate')).exists() ):
            raise serializers.ValidationError( {"slotdate":"Slot with date " + str(validated_data.get('slotdate').strftime("%d-%m-%Y")) + " already exists." })
        vs = self.context['request'].user.vendor_subscription
        total_number_of_slots=validated_data.get('totalavailableslots')
        total_slots_enrolled=validated_data.get('totalenrolled')
        if total_number_of_slots > vs.day_access_slots_per_session:
            raise serializers.ValidationError({"totalavailableslots":"Total available slots can't exceed {number} as per your subscription".format(number=vs.day_access_sessions_per_term)})
        if total_slots_enrolled > vs.day_access_slots_per_session:
            raise serializers.ValidationError({"totalenrolled":"Total available slots can't exceed {number} as per your subscription".format(number=vs.day_access_sessions_per_term)})
        instance = super(SlotSerializer, self).create(validated_data)
        return instance
    
    def update(self, instance, validated_data):
        # location = validated_data.pop('location')
        # validated_data['location'] = models_profile.objects.get(shortname=location)
        if ( instance.slotdate != validated_data.get('slotdate') and models.Slot.objects.filter(slotdate=validated_data.get('slotdate')).exists() ):
            raise serializers.ValidationError( {"date":"Slot with date " + str(validated_data.get('slotdate').strftime("%d-%m-%Y")) + " already exists." })
        vs = self.context['request'].user.vendor_subscription
        total_number_of_slots=validated_data.get('totalavailableslots')
        total_slots_enrolled=validated_data.get('totalenrolled')
        if total_number_of_slots > vs.day_access_slots_per_session:
            raise serializers.ValidationError({"totalavailableslots":"Total available slots can't exceed {number} as per your subscription".format(number=vs.day_access_sessions_per_term)})
        if total_slots_enrolled > vs.day_access_slots_per_session:
            raise serializers.ValidationError({"totalenrolled":"Total available slots can't exceed {number} as per your subscription".format(number=vs.day_access_sessions_per_term)})
        instance = super(SlotSerializer, self).update(instance,validated_data)
        return instance
