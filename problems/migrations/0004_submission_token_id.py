# Generated by Django 3.1.5 on 2021-01-13 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0003_auto_20210106_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='token_id',
            field=models.CharField(max_length=500, null=True),
        ),
    ]