import pytest
from django.urls import reverse
from vendor.subapps.activity_management.models import ActivityAttributeGroups
from vendor.subapps.perticipants.models import EvaluationList, Perticipants

url = reverse('vendor:perticipants:evaluationAdd')


def test_addEvaluation(api_client, vendorUser, activity,  user, location, termActivity, TermActivitySlot, attribute):
    perticipant = Perticipants(
        participant=user,
        activity=activity,
        term_activityslot=termActivity,
        term_slot=TermActivitySlot,
        location=location
    )
    perticipant.save()

    attGroup1 = ActivityAttributeGroups(activity=activity, attribute=attribute)
    attGroup1.save()
    attribute.id = None
    attribute.name = 'attr2'

    attribute.save()
    attGroup2 = ActivityAttributeGroups(activity=activity, attribute=attribute)
    attGroup2.save()

    api_client.force_authenticate(vendorUser)
    validated_data = {'evaluation_data': [
        {
            'perticipant_id': perticipant.id,
            "evaluations": [
                {'evaluation': attGroup1.id, "marks": 5},
                {'evaluation': attGroup2.id, "marks": 5},
            ]
        }
    ]
    }
    resp = api_client.post(url, data=validated_data, format='json')
    # print(resp.data)
    assert resp.status_code == 200
    pert_ev = EvaluationList.objects.filter(perticipant=perticipant).count()
    assert pert_ev == 2

    resp = api_client.post(url, data=validated_data, format='json')
    # print(resp.data)
    assert resp.status_code == 200
    pert_ev = EvaluationList.objects.filter(perticipant=perticipant).count()
    assert pert_ev == 2
    wrong_data = {
        'evaluation_data': [
            {
                'perticipant_id': 100,
                "evaluations": [
                    {'evaluation': attGroup1.id, "marks": 5},
                    {'evaluation': attGroup2.id, "marks": 5},
                ]
            }
        ]
    }
    resp = api_client.post(url, data=wrong_data, format='json')
    assert resp.status_code == 404

    wrong_data = {
        'evaluation': [
            {
                'perticipant_id': 100,
                "evaluations": [
                    {'evaluation': attGroup1.id, "marks": 5},
                    {'evaluation': attGroup2.id, "marks": 5},
                ]
            }
        ]
    }

    resp = api_client.post(url, data=wrong_data, format='json')
    assert resp.status_code == 400

    wrong_data = {
        'evaluation_data': [
            {
                'perticipant_id': perticipant.id,
                "evaluations": {'evaluation': attGroup1.id, "marks": 5}
            }
        ]
    }

    resp = api_client.post(url, data=wrong_data, format='json')
    assert resp.status_code == 400
