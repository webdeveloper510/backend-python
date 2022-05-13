import pytest
from superadmin.subapps.perticipents.serializers import PerticipantsSerializer
from vendor.subapps import perticipants


def test_PerticipantsSerializerForFixedActivity(participant, user, userDetails, vendor):
    user.first_name = 'John'
    user.last_name = 'Doe'
    user.save()
    validated_data = {
        'id': 1,
        'first_name': 'John',
        'last_name': 'Doe',
        'user_id': 'User2010',
        'booking_reference': 'anfsknwio3',
        'vendor_name': vendor.name,
        'vendor_code': vendor.vendor_code,
        'activity_code': participant.activity.code,
        'activity_title': participant.activity.title,
        'country': participant.location.city.country.name,
        'city': participant.location.city.name,
        'location': participant.location.address,
        'date': participant.fixed_time_slot.slotdate,
        'time': None,
        'class_id': None,
        'session_id': participant.fixed_time_slot.session_id

    }

    serializer = PerticipantsSerializer(participant)
    assert serializer.data == validated_data


def test_PerticipantsSerializerForDayAccess(participant, user, userDetails, vendor, day_slot, timeslot):
    user.first_name = 'John'
    user.last_name = 'Doe'
    user.save()
    participant.fixed_time_slot = None

    participant.day_access_slot = day_slot
    participant.day_access_timeslot = timeslot
    participant.save()

    validated_data = {
        'id': 1,
        'first_name': 'John',
        'last_name': 'Doe',
        'user_id': 'User2010',
        'booking_reference': 'anfsknwio3',
        'vendor_name': vendor.name,
        'vendor_code': vendor.vendor_code,
        'activity_code': participant.activity.code,
        'activity_title': participant.activity.title,
        'country': participant.location.city.country.name,
        'city': participant.location.city.name,
        'location': participant.location.address,
        'date': participant.day_access_slot.slotdate,
        'time': None,
        'class_id': None,
        'session_id': participant.day_access_slot.session_id

    }

    serializer = PerticipantsSerializer(participant)
    assert serializer.data == validated_data


def test_PerticipantsSerializerForTermActivity(participant, user, userDetails, vendor, termActivity, TermActivitySlot):
    user.first_name = 'John'
    user.last_name = 'Doe'
    user.save()
    participant.fixed_time_slot = None
    participant.term_activityslot = termActivity
    participant.term_slot = TermActivitySlot
    participant.save()

    validated_data = {
        'id': 1,
        'first_name': 'John',
        'last_name': 'Doe',
        'user_id': 'User2010',
        'booking_reference': 'anfsknwio3',
        'vendor_name': vendor.name,
        'vendor_code': vendor.vendor_code,
        'activity_code': participant.activity.code,
        'activity_title': participant.activity.title,
        'country': participant.location.city.country.name,
        'city': participant.location.city.name,
        'location': participant.location.address,
        'date': participant.term_slot.slotdate,
        'time': participant.term_slot.sttime,
        'class_id': participant.term_activityslot.classid,
        'session_id': participant.term_slot.sessionid

    }

    serializer = PerticipantsSerializer(participant)
    assert serializer.data == validated_data
