from asyncore import read
from django.db.models.query_utils import Q
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from common.methods import calculate_age
from django.contrib.auth.models import User

from common.CustomLimitOffsetPaginator import genarate_rand_int
from vendor.subapps.activity_management import models as ac_model
from vendor.subapps.profile.models import VendorLocation
from vendor.subapps.perticipants.models import Perticipants


class TrialClassSerializer(ModelSerializer):
    activity_code = serializers.CharField(source='activity.code')
    activity_title = serializers.CharField(
        source='activity.title', required=False)
    # location = serializers.CharField(source='location.shortname')
    location_name= serializers.CharField(source='location.shortname', read_only=True)
    userid = serializers.CharField(
        source='participant.userdetails.code', required=False)
    gender = serializers.CharField(
        source='participant.userdetails.gender', required=False)
    requesting_user_id = serializers.CharField(required=True, write_only=True)
    trial_class_userid = serializers.CharField(required=True, write_only=True)
    session = serializers.CharField(required=True, write_only=True)
    full_name = serializers.SerializerMethodField()
    session_id = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    can_add = serializers.BooleanField(
        write_only=True, required=False, default=False)

    class Meta:
        model = Perticipants
        fields = ['id',
                  'activity_code', 'activity_title', 'location', 'session_id', 'requesting_user_id', 'session',
                  'trial_class_userid', 'status', 'date', 'time', 'full_name', 'userid', 'age', 'gender',
                  'booking_reference', 'can_add', 'location_name'
                  ]

    def get_full_name(self, obj):
        return f"{obj.participant.first_name} {obj.participant.last_name}"

    def get_session_id(self, obj):
        if obj.day_access_slot:
            return obj.day_access_slot.session_id
        if obj.fixed_time_slot:
            return obj.fixed_time_slot.session_id

        if obj.term_slot:
            return obj.term_slot.sessionid

        if obj.open_time_slot:
            return None

            # TODO:  Open activity pending

    def get_age(self, obj):
        return calculate_age(obj.participant.userdetails.dob)

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
        # TODO: Open Activity pending

    def make_trial_refarence_no(self):
        integers = genarate_rand_int(10)
        return 'T'+str(integers)

    def get_time(self, obj):
        if obj.term_slot:
            try:
                slot_time = obj.term_slot.sttime
                return slot_time
            except:
                return None

        # TODO: Open Activity pending

    def create(self, validated_data):

        obj = {'type': 'trial_perticipant',
               'booking_reference': self.make_trial_refarence_no()}
        code = validated_data.pop('activity', None)

        loc = validated_data.pop('location', None)
        print(loc)
        requesting_user_id = validated_data.pop('requesting_user_id', None)
        trial_class_userid = validated_data.pop(
            'trial_class_userid', None)  # perticipant
        slot = None
        try:
            activity = ac_model.Activity.objects.get(code=code['code'])
            obj['activity'] = activity

        except Exception as e:
            raise serializers.ValidationError(
                {'activity': 'not found any activity with provided code'})

        if activity.activitytype == 'Day Access':
            sessions = validated_data.pop('session')
            try:
                slot = ac_model.Slot.objects.get(id=sessions)

            except Exception as e:
                raise serializers.ValidationError(
                    {'session': "session can't found"})

            if slot.totalenrolled < slot.totalavailableslots or validated_data['can_add']:
                obj['day_access_slot'] = slot
                slot.totalenrolled = (slot.totalenrolled + 1)
                slot.save()
                try:
                    obj['fixed_time_slot'] = slot.ftslots.all()[0]
                except:
                    pass
            else:
                raise serializers.ValidationError(
                    {'session': 'Session is full'})

        if activity.activitytype == "Fixed Term":
            sessions = validated_data.pop('session')
            try:
                slot = ac_model.Fixedtimingslot.objects.get(id=sessions)
            except Exception as e:
                raise serializers.ValidationError(
                    {'session': "session can't found"})

            if slot.totalenrolled < slot.totalavailableslots or validated_data['can_add']:
                obj['fixed_time_slot'] = slot
                slot.totalenrolled = (slot.totalenrolled + 1)
                slot.save()
            else:
                raise serializers.ValidationError(
                    {'session': 'Session is full'})

        if activity.activitytype == 'Term activity':
            sessions = validated_data.pop('session')
            try:
                slot = ac_model.TermActivitySlot.objects.get(id=sessions)
            except Exception as e:
                raise serializers.ValidationError(
                    {'session': "session can't found"})

            if slot.slot.totalenrolled < slot.slot.totalavailable or validated_data['can_add']:
                obj['term_activityslot'] = slot.slot
                obj['term_slot'] = slot
                slot.slot.totalenrolled = (slot.slot.totalenrolled + 1)
                slot.slot.save()

            else:
                raise serializers.ValidationError(
                    {'session': 'Session is full'})
        try:
            # location = VendorLocation.objects.get(id=loc['shortname'])
            # location = VendorLocation.objects.get(id=loc)
            obj['location'] = loc
        except:
            raise serializers.ValidationError(
                {'location': 'not found location'})
        try:
            perticipant = User.objects.get(
                userdetails__code=trial_class_userid)
            obj['participant'] = perticipant
        except Exception:
            raise serializers.ValidationError(
                {'requesting_user_id': "Can't find with this user id"})
        try:
            perticipant = User.objects.get(
                userdetails__code=requesting_user_id)
            obj['enrolled_by'] = perticipant
        except Exception:
            raise serializers.ValidationError(
                {'requesting_user_id': "Can't find with this user id"})

        instance = Perticipants(**obj)
        instance.save()
        return instance

    def update(self, instance,  validated_data):

        code = validated_data.pop('activity', None)
        loc = validated_data.pop('location', None)
        validated_data.pop('status', None)
        validated_data.pop('booking_reference', None)
        requesting_user_id = validated_data.pop('requesting_user_id', None)
        trial_class_userid = validated_data.pop(
            'trial_class_userid', None)  # perticipant
        if code:
            try:
                activity = ac_model.Activity.objects.get(code=code['code'])

            except Exception as e:
                raise serializers.ValidationError(
                    {'activity': 'not found any activity with provided code'})
            # if instance.activity.activitytype == 'Day Access':
            #     instance.day_access_slot.totalenrolled = instance.day_access_slot.totalenrolled - 1
            #     instance.day_access_slot.save()
            #     instance.day_access_slot = None
            #     instance.day_access_timeslot = None
            # elif instance.activity.activitytype == 'Fixed Term':
            #     instance.fixed_time_slot.totalenrolled = (
            #         instance.fixed_time_slot.totalenrolled - 1)
            #     instance.fixed_time_slot.save()
            #     instance.fixed_time_slot = None
            # elif instance.activity.activitytype == 'Term activity':
            #     instance.term_activityslot.totalenrolled = (
            #         instance.term_activityslot.totalenrolled-1)
            #     instance.term_activityslot.save()
            #     instance.term_activityslot = None
            #     instance.term_slot = None
            instance.activity = activity
            sessions = validated_data.pop('session', None)

            if activity.activitytype == 'Day Access':
                if sessions:
                    try:
                        slot = ac_model.Slot.objects.get(id=sessions)

                    except Exception as e:
                        raise serializers.ValidationError(
                            {'session': "session can't found"})

                    if slot.totalenrolled < slot.totalavailableslots:
                        instance.day_access_slot = slot
                        # slot.totalenrolled = (slot.totalenrolled + 1)
                        # slot.save()
                        try:
                            instance.fixed_time_slot = slot.ftslots.all()[0]
                        except:
                            pass
                    else:
                        raise serializers.ValidationError(
                            {'session': 'Session is full'})

            if activity.activitytype == "Fixed Term":
                if sessions:
                    try:
                        slot = ac_model.Fixedtimingslot.objects.get(
                            id=sessions)
                    except Exception as e:
                        raise serializers.ValidationError(
                            {'session': "session can't found"})

                    if slot.totalenrolled < slot.totalavailableslots:
                        instance.fixed_time_slot = slot
                        # slot.totalenrolled = (slot.totalenrolled + 1)
                        # slot.save()
                    else:
                        raise serializers.ValidationError(
                            {'session': 'Session is full'})

            if activity.activitytype == 'Term activity':
                if sessions:
                    try:
                        slot = ac_model.TermActivitySlot.objects.get(
                            id=sessions)
                    except Exception as e:
                        raise serializers.ValidationError(
                            {'session': "session can't found"})

                    if slot.slot.totalenrolled < slot.slot.totalavailable:
                        instance.term_activityslot = slot.slot
                        instance.term_slot = slot
                        # slot.slot.totalenrolled = (slot.slot.totalenrolled + 1)
                        # slot.slot.save()

                    else:
                        raise serializers.ValidationError(
                            {'session': 'Session is full'})
        if loc:
            try:
                # location = VendorLocation.objects.get(id=loc['shortname'])
                instance.location = loc
            except:
                raise serializers.ValidationError(
                    {'location': 'not found location'})
        if trial_class_userid:

            try:
                perticipant = User.objects.get(
                    userdetails__code=trial_class_userid)
                instance.participant = perticipant
            except Exception:
                raise serializers.ValidationError(
                    {'trial_class_userid': "Can't find with this user id"})
        if requesting_user_id:
            try:
                perticipant = User.objects.get(
                    userdetails__code=requesting_user_id)
                instance.enrolled_by = perticipant
            except Exception:
                raise serializers.ValidationError(
                    {'requesting_user_id': "Can't find with this user id"})

        instance.save()
        return instance
