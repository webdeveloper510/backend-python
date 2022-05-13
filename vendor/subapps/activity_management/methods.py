from rest_framework import serializers
from . import models
from datetime import datetime
from . import serializers_activity as activity_serializer

# Update Field directly from Base64FileField - Used with CustomWritableMethodField
def update_media_field(instance, field, newdata, user, name=None, status="ACTIVE", type=None):
    instancefield = getattr(instance, field)
    if(instancefield):
        instancefield.status="INACTIVE"
        instancefield.deleted_at= datetime.now()
        instancefield.save()
    if(newdata):
        serializer = activity_serializer.MediaSerializer(data={"file":newdata, "name":name, "status":status, 'type':type, 'created_by':'test' if user else None})
        if(serializer.is_valid()):
            media = serializer.save()
            setattr(instance, field, media)
    instance.save()

# Update media using Media Object dictionary - Used with MediaSerializer fields
def update_media_object(instance, field, dict):
    # print(getattr(instance, field))
    instancefield = getattr(instance, field)
    if(instancefield):
        instancefield.status="INACTIVE"
        instancefield.deleted_at= datetime.now()
        instancefield.save()
    if(dict.get("file", None)):
        serializer = activity_serializer.MediaSerializer(
            data={"file": dict['file'], "name": dict['name'], "status": dict['status'], 'type': dict['type'],
                  'created_by': 'test'})
        if (serializer.is_valid()):
            media = serializer.save()
            try:
                setattr(instance, field, media)
            except:
                raise serializers.ValidationError({ "error":'invalid media supplied for file'})
    else:
        setattr(instance, field, None)
    instance.save()
