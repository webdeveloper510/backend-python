from attr import field
import pytest
from vendor.subapps.activity_management.models import Activity

from vendor.subapps.perticipants import models


@pytest.mark.django_db
def test_Perticipant(activity,  user, location, fixedtimingslot, day_slot, timeslot, termActivity, TermActivitySlot):
    all_perticipant = models.Perticipants.objects.all().count()
    assert all_perticipant == 0
    # Day access
    perticipant = models.Perticipants(
        participant=user,
        activity=activity,
        day_access_slot=day_slot,
        day_access_timeslot=timeslot,
        location=location,
    )
    perticipant.save()
    total_perticipant = models.Perticipants.objects.all().count()
    assert total_perticipant == 1
    pert = models.Perticipants.objects.get(activity=activity)
    assert pert.activity.id == activity.id
    assert pert.participant == user
    assert pert.day_access_slot.id == day_slot.id
    assert pert.day_access_timeslot.id == timeslot.id

    # Fixed Timing
    activity.id = None
    activity.activitytype = "Fixed Term"
    activity.save()
    fixedtimingslot.activity = activity
    fixedtimingslot.save()

    perticipant = models.Perticipants(
        participant=user,
        activity=activity,
        fixed_time_slot=fixedtimingslot,
        location=location
    )
    perticipant.save()
    total_perticipant = models.Perticipants.objects.all().count()
    assert total_perticipant == 2
    pert = models.Perticipants.objects.get(activity=activity)
    assert pert.activity.id == activity.id
    assert pert.participant == user
    assert pert.fixed_time_slot.id == fixedtimingslot.id
    
    
    # Term activity 
    activity.id = None
    activity.activitytype = "Term activity"
    activity.save()
    termActivity.activity = activity
    termActivity.save()

    perticipant = models.Perticipants(
        participant=user,
        activity=activity,
        term_activityslot=termActivity,
        term_slot=TermActivitySlot,
        location=location
    )
    perticipant.save()
    total_perticipant = models.Perticipants.objects.all().count()
    assert total_perticipant == 3
    pert = models.Perticipants.objects.get(activity=activity)
    assert pert.activity.id == activity.id
    assert pert.participant == user
    assert pert.term_activityslot.id == termActivity.id
    assert pert.term_slot.id == TermActivitySlot.id
