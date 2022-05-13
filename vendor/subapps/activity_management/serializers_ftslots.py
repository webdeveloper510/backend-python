from rest_framework import serializers
from .models import Fixedtimingslot, Timeslot

class Timeslotserializer(serializers.ModelSerializer):
    class Meta:
        model = Timeslot
        fields = '__all__'

class Fixedtimingslotserializer(serializers.ModelSerializer):
    timeslots = Timeslotserializer(many= True, read_only=True)

    class Meta:
        model = Fixedtimingslot
        fields = ('id','activity', 'location','slotdate',
                  'publishdate','totalenrolled', 'totalavailableslots','timeslots')