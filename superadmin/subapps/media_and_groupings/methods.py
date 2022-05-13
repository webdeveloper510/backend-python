from rest_framework import serializers
from . import models
from datetime import datetime
from .media_serializer import MediaDetailSerializer

# Update Field directly from Base64FileField - Used with CustomWritableMethodField


def update_media_field(instance, field, newdata, name=None, status="ACTIVE", type=None):
    instancefield = getattr(instance, field)
    if(instancefield):
        instancefield.status = "INACTIVE"
        instancefield.deleted_at = datetime.now()
        instancefield.save()
    if(newdata):
        serializer = MediaDetailSerializer(
            data={"file": newdata, "name": name, "status": status, 'type': type})
        if(serializer.is_valid()):
            media = serializer.save()
            setattr(instance, field, media)

        else:
            # print('validation error for : ',field  , str(serializer.errors))
            pass
    else:
        setattr(instance, field, None)
    instance.save(update_fields=[field])

# Update media using Media Object dictionary - Used with MediaSerializer fields


def update_media_object(instance, field, dict):
    instancefield = getattr(instance, field)
    if(instancefield):
        instancefield.status = "INACTIVE"
        instancefield.deleted_at = datetime.now()
        instancefield.save()
    if(dict.get("file", None)):
        try:
            media = models.Media.objects.create(**dict)
            setattr(instance, field, media)
        except:
            raise serializers.ValidationError(
                {"error": 'invalid media supplied for file'})
    else:
        setattr(instance, field, None)
    instance.save(update_fields=[field])
