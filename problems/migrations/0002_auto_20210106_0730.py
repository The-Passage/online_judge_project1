# Generated by Django 3.1.5 on 2021-01-06 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='uploaded_file',
            field=models.FileField(upload_to='problemsdata/submissiondata'),
        ),
    ]