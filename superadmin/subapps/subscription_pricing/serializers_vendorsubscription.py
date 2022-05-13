from rest_framework import serializers
from . import models
from superadmin import custom_serializers_fields as csf
from .serializers_subscriptionpricing import SubscriptionPlanForVendorSubscription, SubscriptionPlanSerializer
from datetime import datetime
import decimal
from decimal import Decimal
from superadmin.subapps.countries_and_cities import models as models_country

class VendorSubscriptionSerializer(serializers.ModelSerializer):
    subscription = SubscriptionPlanForVendorSubscription()
    vendor = serializers.SerializerMethodField()
    vendor_code = serializers.SerializerMethodField()


    subscription_period = csf.ReadWriteSerializerMethodField()
    
    total_subscription_remaining = csf.ReadWriteSerializerMethodField(required=False)
    total_subscription_payable = csf.ReadWriteSerializerMethodField(required=False)

    is_editable = serializers.SerializerMethodField()

    email_sent_at = serializers.DateTimeField(read_only=True)
    # email_sub = csf.ReadWriteSerializerMethodField()
    # email_body = csf.ReadWriteSerializerMethodField()

    class Meta:
        model = models.VendorSubscription
        fields = ('id','vendor','subscription_period', 
        'total_subscription_remaining', 'total_subscription_payable', 
        'status','is_editable','email_sent_at','subscription',
        'term_no_of_activities',
        'term_slots_per_session',
        'term_sessions_per_term',
        'term_pricing',
        'open_no_of_activities',
        'open_slots_per_session',
        'open_sessions_per_term',
        'open_pricing',
        'day_access_no_of_activities',
        'day_access_slots_per_session',
        'day_access_pricing',
        'fixed_no_of_activities',
        'fixed_slots_per_session',
        'fixed_pricing',
        'vendor_code',)

    def get_vendor(self, obj):
        return obj.vendor.vendor_profile.name if obj.vendor and obj.vendor.vendor_profile else ''
    
    def get_vendor_code(self, obj):
        return obj.vendor.userdetails.code if obj.vendor and obj.vendor.userdetails else ''

    def get_total_subscription_remaining(self, obj):
        return obj.get_total_subscription_remaining()

    def get_total_subscription_payable(self, obj):
        return obj.get_total_subscription_payable()
    
    def get_is_editable(self, obj):
        if(obj.status != "SENT"):
            if(models.VendorSubscription.objects.filter(vendor__id=obj.vendor_id, status="SENT").exists() ):
                return False
        return True
    
    def get_pricing_by_activity_types(self, obj):

        obj = obj.subscription

        day_access_pricing = obj.subscription_pricing.filter(activity_type=1)
        fixed_timing = obj.subscription_pricing.filter(activity_type=2)
        term = obj.subscription_pricing.filter(activity_type=3)
        o = obj.subscription_pricing.filter(activity_type=4)

        day_access_pricing = day_access_pricing.first(
        ) if day_access_pricing.exists() else None
        fixed_timing = fixed_timing.first() if fixed_timing.exists() else None
        term = term.first() if term.exists() else None
        o = o.first() if o.exists() else None
        return day_access_pricing, fixed_timing, term, o

    '''
    try nested serializer with serializer fields and custom update method
    '''

    def get_no_of_activities(self, obj):
        # obj = obj.subscription

        day_access, fixed_timing, term, o = self.get_pricing_by_activity_types(
            obj)

        day_access = day_access.no_of_activities if day_access else None
        fixed_timing = fixed_timing.no_of_activities if fixed_timing else None
        term = term.no_of_activities if term else None
        o = o.no_of_activities if o else None

        return {
            "day_access": day_access,
            "fixed_timing": fixed_timing,
            "term": term,
            "open": o,
        }

    def get_subscription_period(self, obj):
        f = obj.start_date.strftime("%d-%m-%Y") if  obj.start_date else None
        to = obj.end_date.strftime("%d-%m-%Y") if  obj.end_date else None
        return {
            "from": f,
            "to": to,
        }

    def update(self, instance, validated_data):
        # print(validated_data)
        vendor = validated_data.pop('vendor')
        no_of_activities = validated_data.pop('no_of_activities')
        subscription_period = validated_data.pop('subscription_period')

        subscription = validated_data.pop('subscription')
        # print(subscription.get('subscription_type'))
        if(subscription.get('subscription_type') != "CUSTOM"):
            # print("not custom")
            validated_data.pop('max_slots_dayaccess')
            validated_data.pop('max_slots_fixedtiming')
            validated_data.pop('max_slots_open')
            validated_data.pop('max_slots_term')


        country = subscription.pop('country')
        # print(country)
        try:
            c = models_country.Country.objects.get(name=country)
            pass
        except:
            raise serializers.ValidationError({"country":"invalid country name"})
        

        # instance.subscription = models.SubscriptionPackage.objects.get(name=subscription.get('name', instance.subscription))
        instance.subscription = models.SubscriptionPackage.objects.create(subscription_type=subscription.get('subscription_type'),
        no_of_locations=subscription.get('no_of_locations'),
            no_of_subadmins=subscription.get('no_of_subadmins'),
            has_trial_class=subscription.get('has_trial_class'),
            has_promotions=subscription.get('has_promotions'),
            has_reports=subscription.get('has_reports'),
            price_per_month=subscription.get('price_per_month'),
            country=c,

            max_slots_dayaccess=subscription.get('max_slots_dayaccess'),
            max_slots_fixedtiming=subscription.get('max_slots_fixedtiming'),
            max_slots_open=subscription.get('max_slots_open'),
            max_slots_term=subscription.get('max_slots_term'),
            
            no_of_media=0,
            baner_credit=0,
            header_credit=0,
            search_word_credit=0,
            )

        day_acess = models.SubscriptionPricing.objects.create(subscription_type=instance.subscription,
                                                  activity_type=1, 
                                                  no_of_activities=no_of_activities.get('day_access'), price=-1)
        fixed_timing = models.SubscriptionPricing.objects.create(subscription_type=instance.subscription,
                                                  activity_type=2, 
                                                  no_of_activities=no_of_activities.get('fixed_timing'), price=-1)
        term = models.SubscriptionPricing.objects.create(subscription_type=instance.subscription,
                                                  activity_type=3, 
                                                  no_of_activities=no_of_activities.get('term'), price=-1)
        o = models.SubscriptionPricing.objects.create(subscription_type=instance.subscription,
                                                  activity_type=4, 
                                                  no_of_activities=no_of_activities.get('open'), price=-1)

        instance.start_date = datetime.strptime(subscription_period.get('from'), '%d-%m-%Y')
        instance.end_date = datetime.strptime(subscription_period.get('to'), '%d-%m-%Y')

        instance.save()
        instance.subscription.save()

        super(VendorSubscriptionSerializer, self).update(
            instance, validated_data)

        return instance

class CustomSubscriptionSerializer(serializers.ModelSerializer):
    subscription = SubscriptionPlanSerializer()

    def create(self,data):
        subscription = data.pop('subscription')
        subscription_instance = models.SubscriptionPackage.objects.create(**subscription)
        instance = self.Meta.model(subscription=subscription_instance,**data)
        for key,value in subscription.items():
            setattr(instance,key,value)
        instance.save()
        return instance


    class Meta:
        model = models.VendorCustomSubscription
        fields = '__all__'



class UpdateVendorSubscriptionSerializer(serializers.ModelSerializer):
    vendor_id = serializers.IntegerField(source='vendor.id')
    vendor_code = serializers.CharField(source='vendor.vendor_code', read_only=True)
    vendor = serializers.SerializerMethodField()

    subscription_type = serializers.ChoiceField(
        choices=models.SUBSCRIPTION_TYPE, source='subscription.subscription_type')
    country = serializers.CharField(source="subscription.country")
    total_locations = serializers.IntegerField(
        source='subscription.no_of_locations')
    total_sub_admins = serializers.IntegerField(
        source='subscription.no_of_subadmins')
    trial_class = serializers.BooleanField(
        source='subscription.has_trial_class')
    promotions_module = serializers.BooleanField(
        source='subscription.has_promotions')
    reports_module = serializers.BooleanField(
        source='subscription.has_reports')
    no_of_activities = csf.ReadWriteSerializerMethodField()

    max_slots_dayaccess = serializers.IntegerField(
        source='subscription.max_slots_dayaccess')
    max_slots_fixedtiming = serializers.IntegerField(
        source='subscription.max_slots_fixedtiming')
    max_slots_open = serializers.IntegerField(
        source='subscription.max_slots_open')
    max_slots_term = serializers.IntegerField(
        source='subscription.max_slots_term')

    subscription_period = csf.ReadWriteSerializerMethodField()
    
    total_subscription_remaining = csf.ReadWriteSerializerMethodField(required=False)
    total_subscription_payable = csf.ReadWriteSerializerMethodField(required=False)

    email_sent_at = serializers.DateTimeField(read_only=True)
    # email_sub = csf.ReadWriteSerializerMethodField()
    # email_body = csf.ReadWriteSerializerMethodField()

    price_per_month = serializers.CharField(source="subscription.price_per_month")

    class Meta:
        model = models.VendorSubscription
        fields = ('id','vendor_id','vendor_code','vendor', 'subscription_type','country', 'total_locations',
                  'total_sub_admins', 'trial_class','promotions_module', 
                  'reports_module', 'max_slots_dayaccess','max_slots_fixedtiming', 
                  'max_slots_open', 'max_slots_term',
                  'no_of_activities', 'subscription_period',
                   'price_per_month', 'total_subscription_remaining', 'total_subscription_payable', 
                   'status','email_sent_at')

    def get_vendor(self, obj):
        return obj.vendor.name if obj.vendor else ''

    def get_total_subscription_remaining(self, obj):
        return obj.get_total_subscription_remaining()

    def get_total_subscription_payable(self, obj):
        return obj.get_total_subscription_payable()
    
    def get_pricing_by_activity_types(self, obj):

        obj = obj.subscription

        day_access_pricing = obj.subscription_pricing.filter(activity_type=1)
        fixed_timing = obj.subscription_pricing.filter(activity_type=2)
        term = obj.subscription_pricing.filter(activity_type=3)
        o = obj.subscription_pricing.filter(activity_type=4)

        day_access_pricing = day_access_pricing.first(
        ) if day_access_pricing.exists() else None
        fixed_timing = fixed_timing.first() if fixed_timing.exists() else None
        term = term.first() if term.exists() else None
        o = o.first() if o.exists() else None
        return day_access_pricing, fixed_timing, term, o

    '''
    try nested serializer with serializer fields and custom update method
    '''

    def get_no_of_activities(self, obj):
        # obj = obj.subscription

        day_access, fixed_timing, term, o = self.get_pricing_by_activity_types(
            obj)

        day_access = day_access.no_of_activities if day_access else None
        fixed_timing = fixed_timing.no_of_activities if fixed_timing else None
        term = term.no_of_activities if term else None
        o = o.no_of_activities if o else None

        return {
            "day_access": day_access,
            "fixed_timing": fixed_timing,
            "term": term,
            "open": o,
        }

    def get_subscription_period(self, obj):
        f = obj.start_date.strftime("%d-%m-%Y") if  obj.start_date else None
        to = obj.end_date.strftime("%d-%m-%Y") if  obj.end_date else None
        return {
            "from": f,
            "to": to,
        }

    def update(self, instance, validated_data):
        # print(validated_data)
        vendor = validated_data.pop('vendor')
        no_of_activities = validated_data.pop('no_of_activities')
        subscription_period = validated_data.pop('subscription_period')

        subscription = validated_data.pop('subscription')
        # print(subscription.get('subscription_type'))
        
        # print( "max_slots_dayaccess",subscription.get('max_slots_dayaccess'))


        country = subscription.pop('country')
        # print(country)
        try:
            c = models_country.Country.objects.get(name=country)
            pass
        except:
            raise serializers.ValidationError({"country":"invalid country name"})
        


        
        instance.subscription.subscription_type=subscription.get('subscription_type')
        instance.subscription.no_of_locations=subscription.get('no_of_locations')
        instance.subscription.no_of_subadmins=subscription.get('no_of_subadmins')
        instance.subscription.has_trial_class=subscription.get('has_trial_class')
        instance.subscription.has_promotions=subscription.get('has_promotions')
        instance.subscription.has_reports=subscription.get('has_reports')
        instance.subscription.price_per_month=subscription.get('price_per_month')
            
        instance.subscription.max_slots_dayaccess=subscription.get('max_slots_dayaccess')
        instance.subscription.max_slots_fixedtiming=subscription.get('max_slots_fixedtiming')
        instance.subscription.max_slots_open=subscription.get('max_slots_open')
        instance.subscription.max_slots_term=subscription.get('max_slots_term')

        instance.subscription.country=c
            
        instance.subscription.no_of_media=0
        instance.subscription.baner_credit=0
        instance.subscription.header_credit=0
        instance.subscription.search_word_credit=0


        day_acess = models.SubscriptionPricing.objects.update_or_create(subscription_type=instance.subscription,
                                                  activity_type=1, 
                                                  defaults={"no_of_activities":no_of_activities.get('day_access'), 
                                                  "price":-1})
        fixed_timing = models.SubscriptionPricing.objects.update_or_create(subscription_type=instance.subscription,
                                                  activity_type=2, 
                                                  defaults={"no_of_activities":no_of_activities.get('fixed_timing'), 
                                                  "price":-1})

        term = models.SubscriptionPricing.objects.update_or_create(subscription_type=instance.subscription,
                                                  activity_type=3, 
                                                  defaults={"no_of_activities":no_of_activities.get('term'), 
                                                  "price":-1})

        o = models.SubscriptionPricing.objects.update_or_create(subscription_type=instance.subscription,
                                                  activity_type=4, 
                                                  defaults={"no_of_activities":no_of_activities.get('open'), 
                                                  "price":-1})

        instance.start_date = datetime.strptime(subscription_period.get('from'), '%d-%m-%Y')
        instance.end_date = datetime.strptime(subscription_period.get('to'), '%d-%m-%Y')

        instance.save()
        instance.subscription.save()
        
        super(UpdateVendorSubscriptionSerializer, self).update(
            instance, validated_data)

        return instance
