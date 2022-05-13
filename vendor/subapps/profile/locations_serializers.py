from rest_framework import serializers

from superadmin.subapps.countries_and_cities.models import City, Region, Area
from .  import models

class vendorlocationSerializers(serializers.ModelSerializer):
    city = serializers.CharField()
    area = serializers.CharField()
    region = serializers.CharField()
    
    class Meta:
        model = models.VendorLocation
        fields = ('id','shortname','address','city', 'region', 'area','status')

    def create(self, validated_data):
        try:
            vendor=self.context["request"].user.vendor_profile
        except models.VendorProfile.DoesNotExist:
            raise serializers.ValidationError({"error":"Vendor Profile Not yet Created."})
        city = validated_data.pop('city')
        region = validated_data.pop('region')
        area = validated_data.pop('area')
        cityobject = City.objects.filter(name=city).first()
        regionobject = Region.objects.filter(name=region).first()
        areaobject = Area.objects.filter(name=area).first()
        instance = models.VendorLocation.objects.create(**validated_data, city=cityobject, region=regionobject, area=areaobject,vendor=vendor)
        return instance

    def update(self, instance, validated_data):
        if 'city' in validated_data :
            city = validated_data.pop('city')
            instance.city = City.objects.get(name=city)
        if 'region' in validated_data:
            region = validated_data.pop('region')
            instance.region = Region.objects.get(name=region)
        if 'area' in validated_data:
            area = validated_data.pop('area')
            instance.area = Area.objects.get(name=area)

        instance.save()
        super(vendorlocationSerializers, self).update(instance, validated_data)
        return instance

