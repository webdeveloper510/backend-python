from django.utils import tree
from rest_framework import serializers
from .models import Coupons,CouponsParticipants
from vendor.subapps.activity_management import models as ac_model


class CouponsSerializer(serializers.ModelSerializer):
    activity_title = serializers.CharField(
        source='activity.title', read_only=True)
    activity_code = serializers.CharField(source='activity.code')
    first_name = serializers.CharField(
        source='created_by.userdetails.firstname', read_only=True)
    last_name = serializers.CharField(
        source='created_by.userdetails.lastname', read_only=True)
    redeemed = serializers.CharField(source='coupons_used', read_only=True)

    class Meta:
        model = Coupons
        fields = ['id', 'activity_title', 'activity_code', 'coupon_code', 'discount_value', 'start_date',
                  'discountType', 'end_date', 'total_coupons', 'coupons_used', 'status', 'first_name',
                  'last_name', 'created_at', 'redeemed'
                  ]

    def create(self, validated_data):
        code = validated_data.pop('activity', None)
        try:
            activity = ac_model.Activity.objects.get(code=code['code'])
            validated_data['activity'] = activity
        except Exception as e:
            raise serializers.ValidationError(
                {'activity': 'not found any activity with provided code'})

        return super().create(validated_data)

    def update(self, instance, validated_data):

        validated_data.pop('activity', None)

        return super().update(instance, validated_data)

class CouponsParticipantsSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    userId = serializers.SerializerMethodField()
    class_id = serializers.SerializerMethodField()
    session_id = serializers.SerializerMethodField()
    commencement_date=serializers.SerializerMethodField()
    commencement_time=serializers.SerializerMethodField()
    bookingRefNo = serializers.SerializerMethodField()

    def get_username(self,obj):
        user = obj.participant.participant
        return user.first_name+' '+user.last_name

    def get_userId(self,obj):
        user = obj.participant.participant
        return user.username
    
    def get_class_id(self,obj):
        activity = obj.coupon.activity
        if activity.type == "Term activity":
            return activity.Activity.classid
        
        return ""
    
    def get_session_id(self,obj):
        activity = obj.coupon.activity
        if activity.type == "Term Activity" or activity.type == "Fixed Term":
            return activity.Activity.session_id
        
        return ""

    def get_commencement_date(self,obj):
        activity= obj.coupon.activity
        if activity.type == "Term Activity":
            return activity.Activity.commencementdate
        
        return ""
    
    def get_commencement_time(self,obj):
        return ""
    
    def get_bookingRefNo(self,obj):
        return obj.participant.booking_reference

    class Meta:
        model = CouponsParticipants
        fields = ("username","userId","class_id","session_id","commencement_date","commencement_time","bookingRefNo")
