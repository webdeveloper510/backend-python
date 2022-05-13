from rest_framework import serializers, status, generics
from .models import Fixedtimingslot, Timeslot
from .serializers_ftslots import  Timeslotserializer, Fixedtimingslotserializer

class FixedSlotsListView(generics.ListCreateAPIView) :
    queryset = Fixedtimingslot.objects.all()
    serializer_class = Fixedtimingslotserializer

class FixedSlotsDetailsView(generics.RetrieveUpdateDestroyAPIView) :
    queryset = Fixedtimingslot.objects.all()
    serializer_class = Fixedtimingslotserializer

class TimeSlotListView(generics.ListCreateAPIView) :
    queryset = Timeslot.objects.all()
    serializer_class = Timeslotserializer

class TimeSlotDetailsView(generics.RetrieveUpdateDestroyAPIView) :
    queryset = Timeslot.objects.all()
    serializer_class = Timeslotserializer