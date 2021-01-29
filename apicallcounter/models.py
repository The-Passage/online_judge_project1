from django.db import models

class ApiCallCount(models.Model):
    call_count = models.IntegerField(default=0)