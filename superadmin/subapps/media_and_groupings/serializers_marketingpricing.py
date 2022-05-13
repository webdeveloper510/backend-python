from rest_framework import serializers
from . import models
from . import methods
from superadmin.subapps.countries_and_cities import models as models_country
from superadmin import custom_serializers_fields as csf


class MarketingSetting(serializers.ModelSerializer):
    city = serializers.CharField()
    # app
    # web
    class Meta:
        model = models.MarketingSettings
        # fields = "__all__"
        fields = ('id','city', 'marketing_type', 'platform_type','catagory')

    # def create(self, validated_data):
    #     city = validated_data.pop('city')
    #     try:
    #         c = models_country.City.objects.get(name=city)
    #     except:
    #         raise serializers.ValidationError({"city":"invalid city name"})
    #     return models.Marketing.objects.create(**validated_data, city=c)
    
    # def update(self, instance, validated_data):
    #     city = validated_data.pop('city', instance.city.name)
    #     try:
    #         c = models_country.City.objects.get(name=city)
    #         instance.city = c
    #     except:
    #         raise serializers.ValidationError({"city":"invalid city name"})
        
    #     instance.save()
    #     super(MarketingSerializer, self).update(instance, validated_data)
    #     return instance