from rest_framework import serializers
from superadmin import custom_serializers_fields as csf
from . import models


class MediaDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    file = csf.CustomBase64FileField()

    class Meta:
        model = models.Media
        fields = '__all__'
