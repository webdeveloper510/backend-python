from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import models
from django.shortcuts import get_object_or_404
from authentication import responses

# For HTTP Error
from rest_framework import status
from . import serializers_avatars as serializers
from django.db.models import ProtectedError

class Avatars(APIView):
    # To allow authenticated users only

    def get(self, request):
        objs = models.Avatar.objects.all()
        serializer = serializers.AvatarSerializer(objs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.AvatarSerializer(data=request.data)
        if (serializer.is_valid()):
            obj = serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Avatar(APIView):
    # To allow authenticated users only

    def delete(self, request, id):
        try:
            obj = models.Avatar.objects.get(id=id)
        except:
            return Response(responses.RESP_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        # media = 
        try:
            if (obj.media):
                obj.media.status = "INACTIVE"
                obj.media.save(update_fields=['status'])
            obj.delete()
            return Response(responses.create_success_response('object deleted successfully'))
        
        except ProtectedError as e:
            return Response(responses.create_failure_response('this avatar is currently being used. ' + str(e) ) )
        
        except:
            return Response(responses.RESP_INTERNAL_SERVER_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)