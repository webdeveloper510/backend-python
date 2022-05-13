from django.conf import settings
from django.core.management.base import BaseCommand
from superadmin.subapps.media_and_groupings import models as models_media
class Command(BaseCommand):
    help = 'Create Media Objects for Standard Logos'

    def handle(self, *args, **kwargs):
        if(not models_media.Media.objects.filter(name = settings.APP_LOGO_MEDIA_NAME, status="ACTIVE").exists()):
            models_media.Media.objects.create(name = settings.APP_LOGO_MEDIA_NAME, status="ACTIVE", type="1")
            # print("APP_LOGO_MEDIA Created")
        else:
            # print("APP_LOGO_MEDIA already exists")
            pass
        
        if(not models_media.Media.objects.filter(name = settings.HEADER_LOGO_MEDIA_NAME, status="ACTIVE").exists()):
            models_media.Media.objects.create(name = settings.HEADER_LOGO_MEDIA_NAME, status="ACTIVE", type="1")
            # print("HEADER_LOGO_MEDIA Created")
        else:
            # print("HEADER_LOGO_MEDIA already exists")
            pass
        
        if(not models_media.Media.objects.filter(name = settings.FULL_LOGO_MEDIA_NAME, status="ACTIVE").exists()):
            models_media.Media.objects.create(name = settings.FULL_LOGO_MEDIA_NAME, status="ACTIVE", type="1")
            # print("FULL_LOGO_MEDIA Created")
        else:
            # print("FULL_LOGO_MEDIA already exists")
            pass
        
        if(not models_media.Media.objects.filter(name = settings.FAVICON_MEDIA_NAME, status="ACTIVE").exists()):
            models_media.Media.objects.create(name = settings.FAVICON_MEDIA_NAME, status="ACTIVE", type="1")
            # print("FAVICON_MEDIA Created")
        else:
            # print("FAVICON_MEDIA already exists")
            pass