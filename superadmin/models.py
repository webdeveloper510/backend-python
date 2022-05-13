from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.db import models

OPERATION_TYPE = (
    ("CREATE","CREATE"),
    ("READ","READ"),
    ("UPDATE","UPDATE"),
    ("DELETE","DELETE"),
)

class DBOperation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="db_operations")
    route = models.CharField(max_length=255, blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    op_type = models.TextField(choices=OPERATION_TYPE ,blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " - " + self.ip_address +" - " + self.route+" - " + self.op_type +" - "+ str(self.timestamp)


class LogRequest(models.Model):
    endpoint = models.CharField(max_length=100, null=True) # The url the user requested
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # User that made request, if authenticated
    response_code = models.PositiveSmallIntegerField() # Response status code
    method = models.CharField(max_length=10, null=True)  # Request method
    remote_address = models.CharField(max_length=20, null=True) # IP address of user
    exec_time = models.IntegerField(null=True) # Time taken to create the response
    date = models.DateTimeField(auto_now=True) # Date and time of request
    body_response = models.TextField() # Response data
    body_request = models.TextField() # Request data