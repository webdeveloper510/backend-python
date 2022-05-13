import base64
import random
import string
import os
from django.conf import settings
from django.core.files.base import File

from superadmin.subapps.vendor_and_user_management.models import Family
from .models import Perticipants
from django.contrib.auth.models import User
from rest_framework import serializers
from . import models
from vendor.subapps.activity_management.models import TermActivitySlot
from vendor.subapps.profile.locations_serializers import vendorlocationSerializers

from superadmin.subapps.vendor_and_user_management.serializers import FamilyUserSerializer, KidSerializer


class participantsSerializer(serializers.ModelSerializer):
    activity_title = serializers.SerializerMethodField()
    activity_code = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    class_id = serializers.SerializerMethodField()
    sessions_id = serializers.SerializerMethodField()

    class Meta:
        model = models.Perticipants
        fields = ['id', 'activity_title', 'activity_code', 'city', 'location',
                  'date', 'time', 'class_id', 'sessions_id', 'booking_reference']

    def get_activity_title(self, obj):
        try:
            name = obj.activity.title
            return name
        except:
            return None

    def get_activity_code(self, obj):
        try:
            name = obj.activity.code
            return name
        except:
            return None

    def get_city(self, obj):
        try:
            city = obj.location.city.name
            return city
        except:
            return None

    def get_location(self, obj):
        try:
            address_location = obj.location.address
            return address_location
        except:
            return None

    def get_date(self, obj):

        if obj.day_access_slot:
            return obj.day_access_slot.slotdate

        if obj.fixed_time_slot:
            return obj.fixed_time_slot.slotdate

        if obj.term_slot:

            try:
                slot_date = obj.term_slot.slotdate
                return slot_date
            except:
                return None
        return None

    def get_time(self, obj):
        if obj.term_slot:
            try:
                slot_time = obj.term_slot.sttime
                return slot_time
            except:
                return None

    def get_class_id(self, obj):
        if obj.day_access_slot or obj.day_access_timeslot or obj.fixed_time_slot:
            return None
        if obj.term_activityslot:

            try:
                class_id = obj.term_activityslot.classid
                return class_id
            except:
                return None
        return None

    def get_sessions_id(self, obj):
        if obj.day_access_slot:
            return obj.day_access_slot.session_id
        if obj.fixed_time_slot:
            return obj.fixed_time_slot.session_id

        if obj.term_slot:
            return obj.term_slot.sessionid

        if obj.open_time_slot:
            return None


class PerticipantListForVendor(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    activity_list = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'user_id', 'activity_list']

    def get_user_id(self, obj):
        return obj.userdetails.code

    def get_activity_list(self, obj):
        participeting_list = obj.perticipant.all()
        serializer = participantsSerializer(participeting_list, many=True)
        return serializer.data


class DayAccessSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = models.Perticipants
        fields = ['id', 'full_name', 'user_id', 'booking_reference']

    def get_full_name(self, obj):
        return f"{obj.participant.first_name} {obj.participant.last_name}"

    def get_user_id(self, obj):
        try:
            return obj.participant.userdetails.code
        except:
            return None


class DayAccessForPastActivitySerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    certificates = serializers.CharField(required=False)

    class Meta:
        model = models.Perticipants
        fields = ['id', 'full_name', 'user_id',
                  'booking_reference', 'certificates']

    def validate_certficates(self, attrs):
        b = attrs.split(';base64,')
        if(len(b) <= 1):
            raise serializers.ValidationError(
                "please provide data:content/type;base64, ")
        return attrs

    def get_full_name(self, obj):
        return f"{obj.participant.first_name} {obj.participant.last_name}"

    def get_user_id(self, obj):
        try:
            return obj.participant.userdetails.code
        except:
            return None

    def save_file(self, strings):
        x = strings
        b = x.split(';base64,')

        a = b[1]

        c = b[0].split('/')

        subDir = 'certificates/'
        file_path = str(settings.MEDIA_ROOT) + '/' + subDir
        if not os.path.isdir(file_path):
            os.makedirs(file_path, mode=0o777)
        randStr = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=6)) + '.' + c[1]
        file_path = file_path + randStr

        d = base64.b64decode(a)
        # print(d)
        decodeit = open(file_path, 'wb')
        decodeit.write(d)
        decodeit.close()

        return subDir + randStr

    def create(self, validated_data):
        certificates = validated_data.pop('certificates', None)
        if certificates:
            file_path = self.save_file(certificates)
            print(file_path)
            validated_data['certificates'] = file_path
        return super().create(validated_data)

    def update(self, instance, validated_data):

        certificates = validated_data.pop('certificates', None)
        if certificates:
            file_path = self.save_file(certificates)
            validated_data['certificates'] = file_path
        return super().update(instance, validated_data)


class EvaluationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EvaluationList
        fields = ['id', 'perticipant', 'marks', 'evaluation']
        extra_kwargs = {'evaluation': {'write_only': True}}


class TermSerializerForPerticipants(serializers.ModelSerializer):
    perticepants = serializers.SerializerMethodField()
    class_id = serializers.SerializerMethodField()
    to_date = serializers.SerializerMethodField()
    from_date = serializers.SerializerMethodField()
    total_perticipants = serializers.SerializerMethodField()

    class Meta:
        model = TermActivitySlot
        fields = ['id', 'from_date', 'to_date', 'class_id', 'sessionid',
                  'total_perticipants', 'perticepants']

    def get_from_date(self, obj):
        return obj.sttime.isoformat()

    def get_to_date(self, obj):
        return obj.edtime.isoformat()

    def get_class_id(self, obj):
        return obj.slot.classid

    def get_total_perticipants(self, obj):
        return obj.termSlotSlotParticipants.all().count()

    def get_perticepants(self, obj):
        perticipants = obj.termSlotSlotParticipants.all()
        serializer = DayAccessSerializer(perticipants, many=True)
        return serializer.data


class SessionsSerializer(serializers.ModelSerializer):
    to_time = serializers.SerializerMethodField()
    from_time = serializers.SerializerMethodField()

    class Meta:
        model = TermActivitySlot
        fields = ['id', 'slotdate', 'from_time', 'to_time', 'sessionid']

    def get_from_time(self, obj):

        return obj.sttime.isoformat()

    def get_to_time(self, obj):
        return obj.edtime.isoformat()


class FamilySerializer(serializers.ModelSerializer):
    superadmin = FamilyUserSerializer()
    admin = FamilyUserSerializer()
    kids = KidSerializer(many=True)

    class Meta:
        model = Family
        fields = ('id','superadmin', 'admin', 'kids', 'status')


class EnrolmentsSerialzer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    from_date = serializers.SerializerMethodField()
    to_date = serializers.SerializerMethodField()
    class_id = serializers.SerializerMethodField()
    sessionid = serializers.SerializerMethodField()

    class Meta:
        model = Perticipants
        fields = ['id', 'title', 'code',
                  'booking_reference', 'class_id', 'sessionid', 'location', 'from_date', 'to_date']

    def get_title(self, obj):
        return obj.activity.title

    def get_from_date(self, obj):
        if obj.day_access_slot:
            return obj.day_access_slot.slotdate

        if obj.fixed_time_slot:
            return obj.fixed_time_slot.slotdate

        # if obj.term_slot:
        #     try:
        #         slot_date = obj.term_slot.slotdate
        #         return slot_date
        #     except:
        #         return None
        return None

    def get_to_date(self, obj):
        if obj.day_access_slot:
            return obj.day_access_slot.slotdate

        if obj.fixed_time_slot:
            return obj.fixed_time_slot.slotdate

        if obj.term_slot:
            try:
                slot_date = obj.term_slot.slotdate
                return slot_date
            except:
                return None
        return None

    def get_code(self, obj):

        return obj.activity.code

    def get_location(self, obj):
        return obj.location.shortname if obj.location else None

    def get_class_id(self, obj):
        if obj.day_access_slot or obj.day_access_timeslot or obj.fixed_time_slot:
            return None
        if obj.term_activityslot:

            try:
                class_id = obj.term_activityslot.classid
                return class_id
            except:
                return None
        return None

    def get_sessionid(self, obj):
        if obj.day_access_slot:
            return obj.day_access_slot.session_id
        if obj.fixed_time_slot:
            return obj.fixed_time_slot.session_id

        if obj.term_slot:
            return obj.term_slot.sessionid

        if obj.open_time_slot:
            return None
