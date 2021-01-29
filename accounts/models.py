from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserDetails(models.Model):
    u_name = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=100, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    institute = models.CharField(max_length=100, blank=True, null=True)
    institute_id = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.u_name.username
