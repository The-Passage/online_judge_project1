from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.

class problemset(models.Model):
    problem_name = models.CharField(max_length=500)
    #problem_author = models.CharField(max_length=300)
    description = RichTextField(blank=True, null=True)
    input_description = RichTextField(blank=True, null=True)
    output_description = RichTextField(blank=True, null=True)
	#problem_file = models.FileField(upload_to='offlineProblemData/problemset', blank=True)
    problem_time_limit = models.FloatField(default=2.0)
    problem_memory_limit = models.IntegerField(default=1024)
    problem_input = models.FileField(upload_to='problemsdata/inputdata/', blank=True)
    problem_output = models.FileField(upload_to='problemsdata/outputdata/', blank=True)
    sample_input = RichTextField(blank=True, null=True)
    sample_output = RichTextField(blank=True, null=True)
    total_solve = models.IntegerField(default=0)
    total_submit = models.IntegerField(default=0)
    special_judge = models.BooleanField(default=False)
    
    def __str__(self):
        return self.problem_name


class submission(models.Model):
    token_id = models.CharField(max_length=100, null=True)
    problem_id = models.ForeignKey(problemset, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    judge_result = models.CharField(max_length=50, default="Submitted")
    submission_time = models.DateTimeField(auto_now_add=True)
    uploaded_file = models.FileField(upload_to='problemsdata/submissiondata/')
    language = models.CharField(max_length=50)