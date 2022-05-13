from rest_framework import serializers, status, generics
from .models import TermActivity, TermActivitySlot
from .serializers_termactivity import TermactivitySerializer, TermactivityslotSerializer


class TermActivityListView(generics.ListCreateAPIView):
    queryset = TermActivity.objects.all()
    serializer_class = TermactivitySerializer

class TermActivitySlotListView(generics.ListCreateAPIView):
    queryset = TermActivitySlot.objects.all()
    serializer_class = TermactivityslotSerializer

class TermActivityDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TermActivity.objects.all()
    serializer_class = TermactivitySerializer

class TermActivitySlotDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TermActivitySlot.objects.all()
    serializer_class = TermactivityslotSerializer
