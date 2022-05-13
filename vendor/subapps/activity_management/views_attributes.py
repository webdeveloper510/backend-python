from rest_framework import serializers, status, generics,views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Attribute, SubAttribute
from .serializers_attributes import AttributeSerializer,SubAttributeSerializer


class AttributeListView(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer

class AttributeDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer

class SubAttributesView(views.APIView):
    permission_classes =[IsAuthenticated]

    def get(self,request,pk):
        subAttributes = SubAttribute.objects.filter(attribute__id=pk)
        return Response(SubAttributeSerializer(subAttributes,many=True).data)