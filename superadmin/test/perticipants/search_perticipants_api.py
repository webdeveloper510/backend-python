import pytest
import json
from django.urls import reverse
from superadmin.subapps.perticipents import serializers
from superadmin.subapps.perticipents.serializers import PerticipantsSerializer, perticipant_models


url = reverse('superadmin:perticipants:search_perticipants')


def make_perticipant(user,  participant, termActivity, TermActivitySlot, day_slot, timeslot):
    user.first_name = 'John'
    user.last_name = 'Doe'
    user.save()

    participant.fixed_time_slot = None
    participant.term_activityslot = termActivity
    participant.term_slot = TermActivitySlot
    participant.save()

    participant.fixed_time_slot = None
    participant.id = None
    participant.day_access_slot = day_slot
    participant.day_access_timeslot = timeslot
    participant.save()


def test_getRequest(api_client, user, userDetails, participant, termActivity, TermActivitySlot, day_slot, timeslot):
    make_perticipant(user, participant,  termActivity,
                     TermActivitySlot, day_slot, timeslot)

    resp = api_client.get(url)
    assert resp.status_code == 200
    resp = resp.json()
    assert resp['count'] == 2

    url1 = url + '?first_name=John'
    resp = api_client.get(url1)
    assert resp.status_code == 200
    new_resp = resp.json()
    assert new_resp['count'] == 2
    perticipatns = perticipant_models.Perticipants.objects.filter(
        participant__first_name='John')
    serializer = PerticipantsSerializer(perticipatns, many=True)

    expected = serializer.data
    assert all([a == b for a, b in zip(new_resp['results'], expected)])

    url1 = url + '?first_name=Johns'
    resp = api_client.get(url1)
    assert resp.status_code == 200
    resp = resp.json()
    assert resp['count'] == 0
