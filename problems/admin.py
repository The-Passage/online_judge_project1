from django.contrib import admin
from problems.models import problemset
from problems.models import submission
# Register your models here.

admin.site.register(problemset)
admin.site.register(submission)

