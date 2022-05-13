from rest_framework import serializers
from . import models
from . import methods
from superadmin import custom_serializers_fields as csf

from django.db import transaction
from django.db import IntegrityError


class AvatarSerializer(serializers.ModelSerializer):
    media = csf.ReadWriteSerializerMethodField(allow_null=True)

    class Meta:
        model = models.Avatar
        fields = '__all__'

    def create(self, validated_data):
        media = validated_data.pop('media', None)
        with transaction.atomic():
            instance = super(AvatarSerializer, self).create(validated_data)
            if (media):
                # print('executed')
                # print(media)
                methods.update_media_field(instance, 'media', newdata=media, name="AVATAR", status="ACTIVE",
                                           type="1")

        return instance

    def update(self, instance, validated_data):
        media = validated_data.pop('media', None)
        super(AvatarSerializer, self).update(instance, validated_data)
        return instance

    def get_media(self, obj):
        return obj.media.file.url if obj.media and obj.media.file else None