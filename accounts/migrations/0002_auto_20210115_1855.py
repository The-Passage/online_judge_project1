# Generated by Django 3.1.5 on 2021-01-15 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='user_profession',
            new_name='UserProfession',
        ),
    ]
