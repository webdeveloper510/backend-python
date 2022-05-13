from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.db import models
from common import email
from django.urls import reverse


# Create your models here.

class UserFeedback(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_feedback')
    feedback = models.TextField(max_length=1000, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


TARGET_RIGHTS = (
    ("CLASS_ENROLMENT", "CLASS_ENROLMENT"),
    ("VIEWING", "VIEWING"),
    ("SUPERUSER", "SUPERUSER"),
)
INVITATION_STATUS = (
    ("CANCEL", "CANCEL"),
    ("ACTIVE", "ACTIVE"),
    ("ACCEPTED", "ACCEPTED"),
)

class UserAdminInvitation(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invitations_sent")
    recepient_email = models.EmailField( null=True, blank=True)
    recepient_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invitations_accepted", null=True, blank=True)
    target_rights = models.CharField(choices=TARGET_RIGHTS, max_length=20, null=True, blank=True)
    token = models.CharField(max_length=70, null=True, blank=True)
    status = models.CharField(choices=INVITATION_STATUS, default='ACTIVE', max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    
    def send_email(self, request):
        link = request.build_absolute_uri( reverse('superadmin:settings:InvitationLandingPage', kwargs={"token":self.token}) )
        subject = "Invitation to join family of user " + self.sender.get_full_name() + " at Moppetto.com"
        message_text = "Mr. " +  self.sender.get_full_name() + " has invited you to join his family. please click this link to accept invitation and create account. link:" + link
        message_html = "Mr. " +  self.sender.get_full_name() + " has invited you to join his family. please click this link to accept invitation and create account." + link
        print(message_text)
        r = email.send_multi_email(self.recepient_email,subject, message_text, message_html )
        print(r)
        if(r != 1):
            return False
        return True





