from rest_framework import serializers

from vendor.subapps.perticipants import models as perticipant_models
from vendor.subapps.activity_management import models as activity_model


class PerticipantsSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        source='participant.first_name')
    last_name = serializers.CharField(
        source='participant.last_name')
    user_id = serializers.CharField(
        source='participant.userdetails.code')
    vendor_name = serializers.CharField(
        source='location.vendor.name')
    vendor_code = serializers.CharField(
        source='location.vendor.vendor_code')
    activity_code = serializers.CharField(
        source='activity.code')
    activity_title = serializers.CharField(
        source='activity.title')

    country = serializers.CharField(
        source='location.city.country.name')
    city = serializers.CharField(
        source='location.city.name')
    location = serializers.CharField(
        source='location.address')
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    class_id = serializers.SerializerMethodField()
    session_id = serializers.SerializerMethodField()

    class Meta:
        model = perticipant_models.Perticipants
        fields = ['id', 'first_name', 'last_name', 'user_id',
                  'vendor_name', 'vendor_code',
                  'activity_code', 'activity_title',
                  'country', 'city', 'location', 'date', 'time',
                  'class_id', 'session_id',
                  'booking_reference'
                  ]

    def get_date(self, obj):
        date = None
        if obj.day_access_slot:
            date = obj.day_access_slot.slotdate

        if obj.fixed_time_slot:
            date = obj.fixed_time_slot.slotdate

        if obj.term_slot:

            try:
                date = obj.term_slot.slotdate

            except:
                return None
        date_time = date.strftime("%Y-%m-%d")
        return date_time

    def get_time(self, obj):
        if obj.term_slot:
            try:
                slot_time = obj.term_slot.sttime
                return slot_time.strftime("%H:%M:%S")
            except:
                return None
        else:
            None

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

    def get_session_id(self, obj):
        if obj.day_access_slot:
            return obj.day_access_slot.session_id  # TODO: ASK TO SUJIT SIR
        if obj.fixed_time_slot:
            return obj.fixed_time_slot.session_id  # TODO: ASK TO SUJIT SIR

        if obj.term_slot:
            return obj.term_slot.sessionid

        if obj.open_time_slot:
            return None  # TODO: ASK TO SUJIT SIR


class DayAccessSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = perticipant_models.Perticipants
        fields = ['id', 'full_name', 'user_id', 'booking_reference']

    def get_full_name(self, obj):
        return f"{obj.participant.first_name} {obj.participant.last_name}"

    def get_user_id(self, obj):
        try:
            return obj.participant.userdetails.code
        except:
            return None


class TermSerializerForPerticipants(serializers.ModelSerializer):
    perticepants = serializers.SerializerMethodField()
    class_id = serializers.SerializerMethodField()
    to_date = serializers.SerializerMethodField()
    from_date = serializers.SerializerMethodField()
    total_perticipants = serializers.SerializerMethodField()

    class Meta:
        model = activity_model.TermActivitySlot
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
