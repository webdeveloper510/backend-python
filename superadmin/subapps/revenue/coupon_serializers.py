from rest_framework import serializers
from django.db import transaction
from . import models
from superadmin.subapps.countries_and_cities.models import Country
from superadmin.subapps.subscription_pricing.models import SubscriptionPackage


class CouponSerialzier(serializers.ModelSerializer):
    country = serializers.CharField(required=True)
    coupon_code = serializers.CharField(required=True)
    subscription = serializers.ListField(write_only=True)
    # subscriptions = serializers.PrimaryKeyRelatedField(many=True, write_only=False, queryset=SubscriptionPackage.objects.all(), source='subscriptions.subscription_type')
    count_of_used_coupon = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    discount_apply_type = serializers.SerializerMethodField()

    class Meta:
        model = models.Coupons
        fields = ("id", "country", "coupon_code", "count_of_used_coupon",
                  "discountType", "discount_value", "from_date", "first_name", "last_name",
                  'subscription', "to_date", "max_number_of_coupon", "status", "created_at",
                  'discount_apply_type'
                  )
        extra_kwargs = {
            'discount_value': {'required': True},
            'max_number_of_coupon': {'required': True},
        }

    def get_created_at(self, obj):
        return obj.created_at.isoformat()

    def get_discount_apply_type(self, obj):
        val = [subs_ins.subscription_type for subs_ins in obj.subscriptions.all()]
        val = ' '.join(val)
        return val

    def get_count_of_used_coupon(self, obj):
        return obj.coupondetails.all().count()

    def get_first_name(self, obj):
        return obj.created_by.first_name if obj.created_by else None

    def get_last_name(self, obj):
        return obj.created_by.last_name if obj.created_by else None

    def create(self, validated_data):
        try:
            country_name = validated_data.pop('country')
            country = Country.objects.get(name=country_name)
        except Exception as e:

            raise serializers.ValidationError(
                {"country": "Country can not found with this name."})

        try:
            subscription = validated_data.pop('subscription')

        except:
            raise serializers.ValidationError(
                {'subscriptions': 'This field is required'})

        coupons = models.Coupons.objects.filter(
            coupon_code=validated_data['coupon_code'])

        if coupons.exists():
            raise serializers.ValidationError(
                {'coupon_code': 'This coupon code already in stored'})

        with transaction.atomic():
            coupon = models.Coupons.objects.create(
                **validated_data, country=country)
            for name in subscription:
                try:
                    subs = SubscriptionPackage.objects.get(
                        subscription_type=name)

                    coupon.subscriptions.add(subs)
                    coupon.save()
                except Exception as e:
                    raise serializers.ValidationError(
                        {'subscriptions': str(e)})
        return coupon

    def update(self, instance, validated_data):
        try:
            validated_data.pop('country', None)
            validated_data.pop('deleted', None)
            subscription = validated_data.pop('subscription', None)
            print(subscription)
            # validated_data.pop('status')

        except Exception as e:
            print(e)
            pass

        try:
            with transaction.atomic():

                instance = super(CouponSerialzier, self).update(
                    instance, validated_data)
                if subscription:
                    instance.subscriptions.clear()
                    for name in subscription:
                        subs = SubscriptionPackage.objects.get(
                            subscription_type=name)

                        instance.subscriptions.add(subs)
                    instance.save()

            return instance
        except Exception as e:
            raise serializers.ValidationError(str(e))


class couponRedemptionDetailsSerializer(serializers.ModelSerializer):
    coupon = CouponSerialzier(many=False, read_only=True)

    class Meta:
        model = models.couponRedemptionDetails
        fields = ['id', 'coupon', 'vendorSubscription']
        extra_kwargs = {
            "vendorSubscription": {'write_only': True}
        }
