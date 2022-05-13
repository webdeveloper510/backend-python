import pytest
from vendor.subapps.activity_management.models import ActivityAttributeGroups
from vendor.subapps.perticipants import serializers
from vendor.subapps.perticipants.serializers import EvaluationListSerializer
from vendor.subapps.perticipants import models


def test_evaluationListSerializer(activity,  user, location, termActivity, TermActivitySlot, attribute):
    perticipant = models.Perticipants(
        participant=user,
        activity=activity,
        term_activityslot=termActivity,
        term_slot=TermActivitySlot,
        location=location
    )
    perticipant.save()

    attGroup = ActivityAttributeGroups(activity=activity, attribute=attribute)
    attGroup.save()

    evalList = models.EvaluationList(
        perticipant=perticipant,
        evaluation=attGroup,
        marks=5
    )
    evalList.save()

    response_data_of_serialzier = {
        'id': evalList.id,
        'perticipant': evalList.evaluation.id,
        'marks': evalList.marks
    }
    serializer = EvaluationListSerializer(evalList)
    assert serializer.data == response_data_of_serialzier


def test_evaluationAddSerializer(activity,  user, location, termActivity, TermActivitySlot, attribute):
    perticipant = models.Perticipants(
        participant=user,
        activity=activity,
        term_activityslot=termActivity,
        term_slot=TermActivitySlot,
        location=location
    )
    perticipant.save()

    attGroup = ActivityAttributeGroups(activity=activity, attribute=attribute)
    attGroup.save()
    # [
    #   {
    #       perticipant_id: 1,
    #       evaluations: [
    #               {'evaluation_id': 1, marks: 5},
    #               {'evaluation_id': 2, marks: 5},
    #           ]
    #   },
    #   {perticipant_id: 1,
    #       evaluations: [
    #           {'evaluation_id': 1, marks: 5},
    #           {'evaluation_id': 2, marks: 5},
    #       ]
    #   }
    # ]

    valid_serializer_data = {
        'perticipant': perticipant.id,
        'marks': 5,
        'evaluation': attGroup.id
    }
    serializer = EvaluationListSerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    # assert serializer.validated_data == valid_serializer_data
    expected = {
        'id': 1,
        'perticipant': perticipant.id,
        'marks': 5,
    }
    serializer.save()
    assert serializer.data == expected
    assert serializer.errors == {}

    total_eval = models.EvaluationList.objects.all().count()
    assert total_eval == 1
