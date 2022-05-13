
from datetime import datetime
from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
from common.CustomLimitOffsetPaginator import genarate_rand_int

from vendor.subapps.activity_management import models as activty_models


MARKETING_STATUS = (
    ("ACTIVE", "ACTIVE"),
    ("SCHEDULED", "SCHEDULED"),
    ("SUSPENDED", "SUSPENDED"),
    ("EXPIRED", "EXPIRED"),
)


class Perticipants(models.Model):

    PERTICIPANTTYPE = (
        ('booked_perticipant', 'booked_perticipant'),
        ('trial_perticipant', 'trial_perticipant')
    )

    type = models.CharField(
        max_length=20, choices=PERTICIPANTTYPE, default='booked_perticipant')
    participant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='perticipant')
    activity = models.ForeignKey(
        activty_models.Activity, on_delete=models.CASCADE, null=True, blank=True)

    # Fixed Time slot table - Fixedtimingslot
    fixed_time_slot = models.ForeignKey(
        activty_models.Fixedtimingslot, on_delete=models.CASCADE, null=True, blank=True, related_name="ftparticipants")
    # Day Access slot table - Slot, Timeslots - Timeslot
    day_access_slot = models.ForeignKey(
        activty_models.Slot, on_delete=models.CASCADE, null=True, blank=True, related_name="dayParticipants")
    # Open Time slot table - Opentimingslot
   
    day_access_timeslot = models.ForeignKey(
        activty_models.Timeslot, on_delete=models.CASCADE, null=True, blank=True, related_name="dayTimeSlotParticipants")
    # Term Activity slot Table - TermActivity, timeslots- TermActivitySlot
    term_activityslot = models.ForeignKey(
        activty_models.TermActivity, on_delete=models.CASCADE, null=True, blank=True, related_name="termParticipants")
    term_slot = models.ForeignKey(
        activty_models.TermActivitySlot, on_delete=models.CASCADE, null=True, blank=True, related_name="termSlotSlotParticipants")
    enrolled_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='enrolled_by', null=True, blank=True)
    location = models.ForeignKey(
        "VendorLocation", on_delete=models.CASCADE, null=True, blank=True, related_name="enrolledLoc")
    booking_reference = models.CharField(max_length=10, null=True, blank=True)
    certificates = models.FileField(
        upload_to='certificates', null=True, blank=True)
    status =  models.CharField(choices=MARKETING_STATUS,
                                       max_length=15, default='SCHEDULED')

    def __str__(self) -> str:
        return f"{self.participant}({self.activity.activitytype})({self.id})"

    def start_date(self):
        today = datetime.today()
        if self.activity.activitytype == 'Day Access':
            dates = self.day_access_slot.slotdate
            print('*************', dates)
            activity_date = datetime(dates.year, dates.month, dates.day)
            return today < activity_date

        elif self.activity.activitytype == 'Fixed Term':
            dates = self.fixed_time_slot.slotdate
            activity_date = datetime(dates.year, dates.month, dates.day)
            return today < activity_date

        elif self.activity.activitytype == 'Term activity':
            date = self.term_activityslot
            time = self.term_slot
            activity_date = datetime(year=date.year, month=date.month,
                                     day=date.day, hour=time.hour, minute=time.minute)
            return today < activity_date
        elif self.activity.activitytype == 'Open Activity':
            return datetime.today()


class EvaluationList(models.Model):
    marks = models.PositiveSmallIntegerField(default=0)
    perticipant = models.ForeignKey(
        Perticipants, on_delete=models.CASCADE, related_name='evperticipants')
    evaluation = models.ForeignKey(
        'vendor.ActivityAttributeGroups', on_delete=models.CASCADE, related_name='evactattr')


def make_trial_refarence_no():
    integers = genarate_rand_int(10)
    return 'T'+str(integers)


class TrialClass(models.Model):
    participant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='trialPerticipant')
    activity = models.ForeignKey(
        activty_models.Activity, on_delete=models.CASCADE, null=True, blank=True)

    # Fixed Time slot table - Fixedtimingslot
    fixed_time_slot = models.ForeignKey(
        activty_models.Fixedtimingslot, on_delete=models.CASCADE, null=True, blank=True, related_name="trilFtparticipants")
    # Open Time slot table - Opentimingslot
    # open_time_slot = models.ForeignKey(
    #     activty_models.Opentimingslot, on_delete=models.CASCADE, null=True, blank=True, related_name="trialOpenparticipants")
    # Day Access slot table - Slot, Timeslots - Timeslot
    day_access_slot = models.ForeignKey(
        activty_models.Slot, on_delete=models.CASCADE, null=True, blank=True, related_name="trialDayParticipants")
    day_access_timeslot = models.ForeignKey(
        activty_models.Timeslot, on_delete=models.CASCADE, null=True, blank=True, related_name="trialDayTimeSlotParticipants")
    # Term Activity slot Table - TermActivity, timeslots- TermActivitySlot
    term_activityslot = models.ForeignKey(
        activty_models.TermActivity, on_delete=models.CASCADE, null=True, blank=True, related_name="trialTermParticipants")
    term_slot = models.ForeignKey(
        activty_models.TermActivitySlot, on_delete=models.CASCADE, null=True, blank=True, related_name="trialTermSlotSlotParticipants")
    enrolled_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='trialEnrolled_by', null=True, blank=True)
    location = models.ForeignKey(
        "VendorLocation", on_delete=models.CASCADE, null=True, blank=True, related_name="trialEnrolledLoc")
    booking_reference = models.CharField(
        max_length=10, default=make_trial_refarence_no(), blank=True)
    status = models.CharField(choices=MARKETING_STATUS,
                              max_length=15, default='SCHEDULED')
