from rest_framework import serializers
from .models import Reviews

from superadmin.subapps.vendor_and_user_management.models import Vendor


class ReviewsSerializer(serializers.ModelSerializer):
    vendor_name = serializers.SerializerMethodField()
    vendor_code = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    activity_title = serializers.SerializerMethodField()
    activity_code = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    review_date = serializers.SerializerMethodField()

    class Meta:
        model = Reviews
        fields = ('id', 'review', 'ratings', 'response', 'activity', 'status', 'review_date',
                  'vendor_name', 'vendor_code', 'country', 'activity_title', 'activity_code', 'user_name', 'user_id'
                  )

    def get_vendor_name(self, obj):
        user = obj.activity.created_by
        try:
            vendor = Vendor.objects.get(user=user)
            return vendor.name
        except Vendor.DoesNotExist:
            return None

    def get_vendor_code(self, obj):
        user = obj.activity.created_by
        try:
            vendor = Vendor.objects.get(user=user)
            return vendor.vendor_code

        except Vendor.DoesNotExist:
            return None

    def get_country(self, obj):
        user = obj.activity.created_by
        try:
            vendor = Vendor.objects.get(user=user)
            return vendor.country.name
        except:
            return None

    def get_activity_title(self, obj):
        return obj.activity.title if obj.activity else None

    def get_activity_code(self, obj):
        return obj.activity.code if obj.activity else None

    def get_user_name(self, obj):
        return obj.reviewed_by.username if obj.reviewed_by else None

    def get_user_id(self, obj):
        return obj.reviewed_by.userdetails.id if obj.reviewed_by else None

    def get_review_date(self, obj):
        return obj.created_at.isoformat()

    def create(self, validated_data):
        try:
            validated_data.pop('response', None)
        except:
            pass
        print(validated_data['activity'])
        instance = super(ReviewsSerializer, self).create(validated_data)

        return instance


class VendorReviewSerializer(serializers.ModelSerializer):
    activity_title = serializers.SerializerMethodField()
    activity_code = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model =Reviews
        fields = ['id', 'activity_title', 'activity_code', 'location',
                  'username', 'user_id', 'created_at', 'ratings',  'review', 'response']
        extra_kwargs = {
            'ratings': {"read_only": True},
            'review': {"read_only": True}
        }

    def get_activity_title(self, obj):
        return obj.activity.title

    def get_activity_code(self, obj):
        return obj.activity.code

    def get_location(self, obj):
        return 'Suntec City Convention Centre'

    def get_username(self, obj):
        return obj.reviewed_by.username

    def get_user_id(self, obj):
        return str(obj.reviewed_by.userdetails.id) if obj.reviewed_by else None

    def get_created_at(self, obj):
        return obj.created_at.isoformat()
