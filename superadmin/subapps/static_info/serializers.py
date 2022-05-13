from django.conf import settings

from rest_framework import serializers

from superadmin import custom_serializers_fields as csf
from . import models
from superadmin.subapps.media_and_groupings import models as models_media
from superadmin.subapps.countries_and_cities import models as models_country
from superadmin.subapps.media_and_groupings import methods as mediamethods


class StaticContentSerializer(serializers.ModelSerializer):
    link=serializers.SerializerMethodField()

    def get_link(self,obj):
        return '/info/{name}/{country}/{language}'.format(name=obj.resource.name,country=obj.resource.country.name,language=obj.language)
    class Meta:
        model=models.StaticContent
        fields=('id','language','content','link')
class StaticResourceSerializer(serializers.ModelSerializer):
    # Used by Subscription Pricing
    content=StaticContentSerializer(many=True,read_only=True)
    contentData=serializers.CharField(write_only=True)
    contentLanguage=serializers.CharField(write_only=True)
    languageBeforeEdit=serializers.CharField(write_only=True,required=False)
    country=serializers.CharField(write_only=True)


    def create(self,validated_data):

        try:
            country = models_country.Country.objects.get(name=validated_data.get('country'))
        except models_country.Country.DoesNotExist:
            raise serializers.ValidationError({"country":"Country Doesn't exists."})
        language = validated_data.get('contentLanguage')
        data = validated_data.get('contentData')
        resourceData,_ = models.StaticResource.objects.get_or_create(name=validated_data.get("name"),country=country)
        contentData,_ = resourceData.content.get_or_create(language=language)
        contentData.content=data
        contentData.save()
        return resourceData        

    class Meta:
        model = models.StaticResource
        fields = ("country", "name","content",'contentData','contentLanguage','languageBeforeEdit',)


class LogoSerializer(serializers.Serializer):
    app_logo = csf.ReadWriteSerializerMethodField('get_app_logo', allow_null=True)
    header_logo = csf.ReadWriteSerializerMethodField(allow_null=True)
    full_logo = csf.ReadWriteSerializerMethodField(allow_null=True)
    favicon = csf.ReadWriteSerializerMethodField(allow_null=True)

    def __init__(self, *args, **kwargs):
        if('user' in kwargs.keys()):
            self.user = kwargs.pop('user')
        else:
            self.user=None
        super().__init__(*args, **kwargs)

    def get_app_logo(self, obj):
        print('executed')
        media = models_media.Media.objects.get(name = settings.APP_LOGO_MEDIA_NAME)
        return media.file.url

    def get_header_logo(self, obj):
        media = models_media.Media.objects.get(name = settings.HEADER_LOGO_MEDIA_NAME)
        return media.file.url

    def get_full_logo(self, obj):
        media = models_media.Media.objects.get(name = settings.FULL_LOGO_MEDIA_NAME)
        return media.file.url

    def get_favicon(self, obj):
        print('executed')
        media = models_media.Media.objects.get(name = settings.FAVICON_MEDIA_NAME)
        print(media)
        return media.file.url