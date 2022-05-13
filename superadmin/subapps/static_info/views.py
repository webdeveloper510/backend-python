from django.shortcuts import get_object_or_404
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status   # For HTTP Error

from common.CustomLimitOffsetPaginator import CustomLimitOffsetPaginator
from . import serializers
from . import models
from . import methods
from superadmin.subapps.media_and_groupings import models as models_media


from rest_framework import status
from django.db.models import ProtectedError

class StaticResourceList(APIView):
    # To allow authenticated users only
    #permission_classes = (IsAuthenticated,)

    def get(self, request,name):
        objs = models.StaticResource.objects.filter(name=name)
        if('country' in request.GET):
            cname = request.GET['country']
            objs = objs.filter(country__name = cname)
        else:
            return Response({"error":"Country attribute not supplied."},status=status.HTTP_400_BAD_REQUEST)

        if objs.exists():
            serializer = serializers.StaticResourceSerializer(objs.first())
            response = serializer.data
        else:
            response={
                "name":name,
                "content":[]
            }

        if 'language' in request.GET:
            response.pop('content')
            content = objs.first().content.filter(language=request.GET['language'])
            response['content'] = serializers.StaticContentSerializer(content,many=True).data
        return Response(response)
    
    def post(self, request,name):
        request.data["name"] = name
        serializer = serializers.StaticResourceSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"message":"Static info for "+ name +" updated successfully."})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaticContent(APIView):
    # To allow authenticated users only
    permission_classes = (IsAuthenticated,)

    def put(self, request, id):
        try:
            obj = models.StaticContent.objects.get(id=id)
        except:
            return Response({"error":"Static Content Not Found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.StaticContentSerializer(obj, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        obj = models.StaticContent.objects.filter(id=id)
        
        if not obj.exists():
            return Response({"error":"Static Content Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        obj.delete()

        return Response({"message":"Static Content Deleted Successfully."})
        





class Logo(APIView):
    # To allow authenticated users only
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        app_logo = models_media.Media.objects.get(name = settings.APP_LOGO_MEDIA_NAME)
        header_logo = models_media.Media.objects.get(name = settings.HEADER_LOGO_MEDIA_NAME)
        full_logo = models_media.Media.objects.get(name = settings.FULL_LOGO_MEDIA_NAME)
        favicon = models_media.Media.objects.get(name = settings.FAVICON_MEDIA_NAME)
        data = {
            'app_logo':app_logo.file.url if app_logo.file else None,
            'header_logo':header_logo.file.url if header_logo.file else None,
            'full_logo':full_logo.file.url if full_logo.file else None,
            'favicon':favicon.file.url if favicon.file else None,
        }
        return Response(data)

    def patch(self, request):

        response={}
        if('app_logo' in request.data):
            app_logo_data = request.data.get('app_logo', None)
            app_logo = models_media.Media.objects.get(name=settings.APP_LOGO_MEDIA_NAME)
            response['app_logo'] = methods.update_logos(app_logo,app_logo_data, request.user )
        
        if('header_logo' in request.data):
            header_logo_data = request.data.get('header_logo', None)
            header_logo = models_media.Media.objects.get(name=settings.HEADER_LOGO_MEDIA_NAME)
            response['header_logo'] = methods.update_logos(header_logo,header_logo_data, request.user )
        
        if('full_logo' in request.data):
            full_logo_data = request.data.get('full_logo', None)
            full_logo = models_media.Media.objects.get(name=settings.FULL_LOGO_MEDIA_NAME)
            response['full_logo'] = methods.update_logos(full_logo,full_logo_data, request.user )
        
        if('favicon' in request.data):
            favicon_data = request.data.get('favicon', None)
            favicon = models_media.Media.objects.get(name=settings.FAVICON_MEDIA_NAME)
            response['favicon'] = methods.update_logos(favicon,favicon_data, request.user )

        return Response(response)
         