# Generated by Django 3.1.5 on 2021-01-26 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0007_auto_20210124_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='contest_password',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
