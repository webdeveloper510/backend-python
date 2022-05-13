from rest_framework import serializers
from . import models
from . import methods
from superadmin.subapps.countries_and_cities import models as models_country
from superadmin import custom_serializers_fields as csf

class MarketingSerializer(serializers.ModelSerializer):
    city = serializers.CharField()
    class Meta:
        model = models.Marketing
        fields = ('id','from_date', 'to_date', 'type','vendor', 'target_activity', 'city', 'platform_type', 'status')

    def create(self, validated_data):
        city = validated_data.pop('city')
        try:
            c = models_country.City.objects.get(name=city)
        except:
            raise serializers.ValidationError({"city":"invalid city name"})
        return models.Marketing.objects.create(**validated_data, city=c)
    
    def update(self, instance, validated_data):
        city = validated_data.pop('city', instance.city.name)
        try:
            c = models_country.City.objects.get(name=city)
            instance.city = c
        except:
            raise serializers.ValidationError({"city":"invalid city name"})
        
        instance.save()
        super(MarketingSerializer, self).update(instance, validated_data)
        return instance

class BannerMarketingSerializer(serializers.ModelSerializer):
    city = serializers.CharField()
    category = serializers.CharField(source='banner_details.catagory')
    # app_image = csf.ReadWriteSerializerMethodField(source='banner_details.app_image',allow_null=True, write_only=True)
    # web_image = csf.ReadWriteSerializerMethodField(source='banner_details.web_image',allow_null=True, write_only=True)
    vendor_name = serializers.SerializerMethodField()
    # vendor_id = serializers.SerializerMethodField()
    vendor_code = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField()

    
    class Meta:
        model = models.Marketing
        fields = ('id', 'city',  'transaction_id', 'from_date', 'to_date', 'category', 'vendor_name','vendor_code', 'platform_type', 'status', 'media')
    
    # def get_app_image(self, obj):
    #     return obj.banner_details.app_image.file.url if obj.banner_details.app_image else None
    
    # def get_web_image(self, obj):
    #     return obj.banner_details.web_image.file.url if obj.banner_details.web_image else None

    def get_vendor_name(self, obj):
        return obj.vendor.name if obj.vendor else None
    
    # def get_vendor_id(self, obj):
    #     return obj.vendor.id if obj.vendor else None
    
    def get_vendor_code(self, obj):
        return obj.vendor.vendor_details.code if obj.vendor and obj.vendor.vendor_details else None

    def get_media(self, obj):
        platform = self.context['platform_type']
        if platform == 'WEB':
            return obj.banner_details.web_image.file.url if obj.banner_details.web_image else None
        else:
            return obj.banner_details.app_image.file.url if obj.banner_details.app_image else None

class SuperAdminBannerSerializer(serializers.ModelSerializer):
    city = serializers.CharField()
    category = serializers.CharField()
    platform_type = serializers.CharField(required=True)
    media = csf.ReadWriteSerializerMethodField(allow_null=True)
    
    class Meta:
        model = models.AdminBanner
        fields = ('id', 'city','category', 'platform_type','media')
    
    def get_media(self, obj):
        return obj.media.file.url if obj.media else None

    def __init__(self, *args, **kwargs):
        if('user' in kwargs.keys()):
            self.user = kwargs.pop('user')
        else:
            self.user=None
        
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        media = validated_data.pop('media', None )
        category = validated_data.pop('category')
        try:
            cat = models.Category.objects.get(id=category)
        except:
            raise serializers.ValidationError({"category":"invalid category id"})
        
        city = validated_data.pop('city')
        try:
            c = models_country.City.objects.get(name=city)
        except:
            raise serializers.ValidationError({"city":"invalid city id"})
        
        max_count = models.MarketingSettings.objects.filter(marketing_type="BANNER",platform_type=validated_data.get('platform_type'), city=c)
        if(max_count.exists()):
            max_count = max_count.first()
            pass
        else:
            max_count = models.MarketingSettings.objects.create(marketing_type="BANNER",platform_type=validated_data.get('platform_type'), city=c, max_count=5 )

        banner_count = models.AdminBanner.objects.filter(category=cat, city=c, platform_type=validated_data.get('platform_type') ).count()
        if( banner_count >= max_count.max_count):
            raise serializers.ValidationError({"error":"maximum permitted banners are being exceeded. maximum permitted banners are " + str(max_count.max_count)})
        instance = models.AdminBanner.objects.create(**validated_data, category=cat, city=c)

        if (media): 
            methods.update_media_field(instance, 'media', newdata=media,   name="ADMIN_BANNER", status="ACTIVE", type="1")

        return instance
    
    def update(self, instance, validated_data):
        if 'media' in validated_data.keys(): 
            media = validated_data.pop('media', None )
            methods.update_media_field(instance, 'media', newdata=media, name="ADMIN_BANNER", status="ACTIVE", type="1")
        
        instance.save()
        # super(CategorySerializer, self).update(instance, validated_data)
        return instance


class HomepageHeaderMarketingSerializer(serializers.ModelSerializer):
    city = serializers.CharField()
    vendor_name = serializers.SerializerMethodField()
    vendor_id = serializers.SerializerMethodField()
    vendor_code = serializers.SerializerMethodField()
    homepageHeader = serializers.SerializerMethodField()
    class Meta:
        model = models.Marketing
        fields = (
                'id', 'city','vendor_id', 'from_date', 'to_date', 'vendor_name', 'homepageHeader',
                'vendor_code', 'platform_type', 'status')
    
    def get_vendor_name(self, obj):
        return obj.vendor.name if obj.vendor else None
    
    def get_vendor_id(self, obj):
        return obj.vendor.id if obj.vendor else None
    
    def get_vendor_code(self, obj):
        return obj.vendor.vendor_details.code if obj.vendor and obj.vendor.vendor_details else None

    def get_homepageHeader(self, obj):
        return obj.header_details.text if obj.header_details else ''

class SuperAdminHomepageHeaderSerializer(serializers.ModelSerializer):
    city = serializers.CharField(required=True)
    text = serializers.CharField(required=True)
    platform_type = serializers.CharField(required=True)
    class Meta:
        model = models.DefaultHeader
        fields = ('id', 'city', 'platform_type','text', 'date')
    

    def __init__(self, *args, **kwargs):
        if('user' in kwargs.keys()):
            self.user = kwargs.pop('user')
        else:
            self.user=None
        try:
            context = kwargs.get('context')
            if context['method'] == 'GET':
                del self.fields['date']
        except:
            pass
        
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        city = validated_data.pop('city')
        try:
            c = models_country.City.objects.get(name=city)
        except:
            raise serializers.ValidationError({"city":"invalid city id"})
        
        max_count = models.MarketingSettings.objects.filter(marketing_type="HEADER",platform_type=validated_data.get('platform_type'), city=c)
        if(max_count.exists()):
            max_count = max_count.first()
            pass
        else:
            max_count = models.MarketingSettings.objects.create(marketing_type="HEADER",platform_type=validated_data.get('platform_type'), 
                                                        city=c, max_count=5 )

        banner_count = models.DefaultHeader.objects.filter(city=c, platform_type=validated_data.get('platform_type'), date=validated_data.get('date') ).count()
        if( banner_count >= max_count.max_count):
            raise serializers.ValidationError({"error":"maximum permitted headers are being exceeded. maximum permitted headers are " + str(max_count.max_count)})
        instance = models.DefaultHeader.objects.create(**validated_data, city=c)

        return instance

