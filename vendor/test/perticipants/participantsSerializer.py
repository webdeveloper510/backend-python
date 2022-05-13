import pytest
from vendor.subapps.perticipants.serializers import participantsSerializer, Perticipants


def test_valid_day_accessPerticipant(activity,  user, location,  day_slot, timeslot):

    perticipant = Perticipants(
        participant=user,
        activity=activity,
        day_access_slot=day_slot,
        day_access_timeslot=timeslot,
        location=location,
    )
    perticipant.save()

    day_access_validate_data = {
        'id': perticipant.id,
        'activity_title': activity.title,
        'activity_code': activity.code,
        'city': perticipant.location.city.name,
        'location': perticipant.location.address,
        'date': perticipant.day_access_slot.slotdate,
        'time': None,
        'class_id': None,
        'sessions_id': perticipant.day_access_slot.session_id,
        'booking_reference': None

    }
    serializer = participantsSerializer(perticipant)
    assert serializer.data == day_access_validate_data


def test_fixedActivity_serializer(activity,  user, location, fixedtimingslot, termActivity, TermActivitySlot):

    activity.id = None
    activity.activitytype = "Fixed Term"
    activity.save()
    fixedtimingslot.activity = activity
    fixedtimingslot.save()

    perticipant = Perticipants(
        participant=user,
        activity=activity,
        fixed_time_slot=fixedtimingslot,
        location=location
    )
    perticipant.save()

    day_access_validate_data = {
        'id': perticipant.id,
        'activity_title': activity.title,
        'activity_code': activity.code,
        'city': perticipant.location.city.name,
        'location': perticipant.location.address,
        'date': perticipant.fixed_time_slot.slotdate,
        'time': None,
        'class_id': None,
        'sessions_id': perticipant.fixed_time_slot.session_id,
        'booking_reference': None
    }

    serializer = participantsSerializer(perticipant)
    print(serializer.data)
    assert serializer.data == day_access_validate_data


def test_termActivity_serializer(activity,  user, location, termActivity, TermActivitySlot):

    activity.id = None
    activity.activitytype = "Term activity"
    activity.save()
    termActivity.activity = activity
    termActivity.save()

    perticipant = Perticipants(
        participant=user,
        activity=activity,
        term_activityslot=termActivity,
        term_slot=TermActivitySlot,
        location=location
    )
    perticipant.save()

    day_access_validate_data = {
        'id': perticipant.id,
        'activity_title': activity.title,
        'activity_code': activity.code,
        'city': perticipant.location.city.name,
        'location': perticipant.location.address,
        'date': perticipant.term_slot.slotdate,
        'time': perticipant.term_slot.sttime,
        'class_id': perticipant.term_activityslot.classid,
        'sessions_id': perticipant.term_slot.sessionid,
        'booking_reference': None
    }

    serializer = participantsSerializer(perticipant)
    assert serializer.data == day_access_validate_data
