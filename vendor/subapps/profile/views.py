from rest_framework import serializers, status,viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from common.CustomLimitOffsetPaginator import CustomLimitOffsetPaginator
from . import locations_serializers as serializers
from . import profile_serializers
from . import models


class VendorLocation(APIView) :
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = serializers.vendorlocationSerializers(data=request.data,context={"request":request})
        if (serializer.is_valid()):
            obj = serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        paginator = CustomLimitOffsetPaginator()
        obj = request.user.vendor_profile.locations.all()
        page = paginator.paginate_queryset(obj, request, view=self)
        serializer = serializers.vendorlocationSerializers(page, many=True)
        return paginator.get_paginated_response(serializer.data)

class VendorLocationid(APIView):
    permission_classes = (IsAuthenticated,)


    def put(self, request, id):
        try:
            vdobj = request.user.vendor_profile.locations.get(id=id)
        except models.VendorLocation.DoesNotExist:
            return Response({"error":"Location not Found"},status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.vendorlocationSerializers(vdobj, data=request.data, partial=True)
        if (serializer.is_valid()):
            obj = serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        try:
            obj = request.user.vendor_profile.locations.get(id=id)
        except models.VendorLocation.DoesNotExist:
            return Response({"error":"Location not Found"},status=status.HTTP_404_NOT_FOUND) 
        serializer = serializers.vendorlocationSerializers(obj)
        return Response(serializer.data)

class ChangePasswordView(APIView):
    permission_classes=[IsAuthenticated]
    serializer_class = profile_serializers.ChangePasswordSerializer

    def post(self,request,*args,**kwargs):
        serializer = self.serializer_class(data=request.data,context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message":"Password Changed Successfully!"
        })

class ChangeNameView(APIView):
    permission_classes=[IsAuthenticated]
    serializer_class=profile_serializers.ChangeNameSerializer

    def post(self,request,*args,**kwagrs):
        serializer = self.serializer_class(data=request.data,context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message":"Name Changed Successfully!"
        })

class VendorProfileView(APIView):
    serializer_class = profile_serializers.VendorProfileSerializer
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        try:
            res = self.request.user.vendor_profile
            print("bnkkb",res)
        except:
            return Response({
                "message":"Profile Not yet Updated."
            })
        
        return Response(self.serializer_class(res).data)
    
    def post(self,request):
        serializer=self.serializer_class(data=request.data,context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message":"Profile Created Successfully!"
        })
    
    def put(self,request):
        venobj=models.VendorProfile.objects.get(vendor=request.user)
        serializer=self.serializer_class(venobj,data=request.data,context={"request":request},partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message":"Profile Updated Successfully!"
        })



