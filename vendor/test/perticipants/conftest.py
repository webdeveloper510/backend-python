import pytest
from datetime import date, datetime
from superadmin.subapps.media_and_groupings.models import Attribute
from vendor.subapps.activity_management import models as activity_models
from vendor.subapps.profile.models import VendorLocation


@pytest.fixture
def attribute(superAdmin):
    attr = Attribute(
        name='attr1'
    )
    attr.save()
    return attr


@pytest.fixture
def activity(vendor, vendorUser):
    return activity_models.Activity.objects.create(
        title='activity title',
        code='adf',
        description='description',
        activitytype="Day Access",
    )


@pytest.fixture
def location(vendor, city, region, area):
    loc = VendorLocation(
        vendor=vendor,
        shortname='short',
        address='pune, mh, 411014',
        city=city,
        region=region,
        area=area
    )

    loc.save()
    return loc


@pytest.fixture
def fixedtimingslot(activity, location):
    today = date.today()
    ft = activity_models.Fixedtimingslot(
        activity=activity, location=location, slotdate=today, publishdate=today)
    ft.save()
    return ft


# class ActivityAttributeGroups(models.Model):
#     activity = models.ForeignKey(
#         Activity, on_delete=models.CASCADE, related_name='activityAttr')
#     attribute = models.ForeignKey(
#         'superadmin.Attribute', on_delete=models.CASCADE, related_name='activityAttr')

@pytest.fixture
def day_slot(activity, location):
    today = date.today()
    slt = activity_models.Slot(
        activity=activity,
        location=location,
        slotdate=today,
        publishdate=today,
        totalenrolled=0,
        totalavailableslots=10,
        session_id='asd43'
    )
    slt.save()
    return slt


@pytest.fixture
def timeslot(day_slot):
    actTimeSlot = activity_models.Timeslot(
        slot=day_slot,
        from_time='18:00',
        to_time='20:00'
    )
    actTimeSlot.save()
    return actTimeSlot


@pytest.fixture
def termActivity(activity, location):
    actTerm = activity_models.TermActivity(
        activity=activity,
        location=location,
        name='term activity',
        classid='call23',
        totalenrolled=1,
        totalavailable=10,
    )
    actTerm.save()
    return actTerm


@pytest.fixture
def TermActivitySlot(termActivity):
    today = date.today()
    actTerm = activity_models.TermActivitySlot(
        slot=termActivity,
        sessionid='aser453',
        slotdate=today,
        sttime='18:00:00',
        edtime='19:00:00'
    )
    actTerm.save()
    return actTerm
