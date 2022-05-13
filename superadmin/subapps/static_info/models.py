from django.contrib.auth import get_user_model
User = get_user_model()
from django.db import models
# Create your models here.

STATUS = (
    ("1", "ACTIVE"),
    ("2", "INACTIVE"),
)

class StaticResource(models.Model):
    country = models.ForeignKey('Country', on_delete=models.SET_NULL,null=True,blank=True,related_name='staticresources')
    name = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(choices=STATUS, max_length=1, null=True, blank=True)

    def __str__(self):
        return self.name

class StaticContent(models.Model):
    resource = models.ForeignKey(StaticResource,on_delete=models.CASCADE,related_name="content",null=True,blank=True)
    content = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=120, default="Main")
