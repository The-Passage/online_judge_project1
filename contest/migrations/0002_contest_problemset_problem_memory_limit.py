# Generated by Django 3.1.5 on 2021-01-19 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest_problemset',
            name='problem_memory_limit',
            field=models.IntegerField(default=1024),
        ),
    ]
