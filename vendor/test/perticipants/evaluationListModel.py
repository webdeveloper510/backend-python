import pytest
from django.db.utils import IntegrityError
from django.db import transaction
# from vendor.subapps.perticipants import models
from vendor.subapps.perticipants import models
from vendor.subapps.activity_management.models import ActivityAttributeGroups


def test_EvaluationList_model(activity,  user, location, termActivity, TermActivitySlot, attribute):
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
        evaluation=attGroup
    )
    evalList.save()
    totalEvaluation = models.EvaluationList.objects.all().count()
    assert totalEvaluation == 1
    evList = models.EvaluationList.objects.all()
    assert evList[0].marks == 0
    with transaction.atomic():
        try:
            evalList1 = models.EvaluationList(
                marks=-1,
                perticipant=perticipant,
                evaluation=attGroup
            )

            evalList1.save()
        except IntegrityError:
            pass

    totalEvaluation = models.EvaluationList.objects.all().count()
    assert totalEvaluation == 1
