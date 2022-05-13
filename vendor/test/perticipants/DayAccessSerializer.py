import pytest
from vendor.subapps.perticipants.serializers import DayAccessSerializer, Perticipants


def test_dayAccessSerializer(activity,  user, location,  day_slot, timeslot):
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
        'full_name': f"{user.first_name} {user.last_name}",
        'booking_reference': None,
        'user_id': perticipant.participant.userdetails.code
    }
    serializer = DayAccessSerializer(perticipant)
    assert serializer.data == day_access_validate_data
