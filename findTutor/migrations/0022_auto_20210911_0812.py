# Generated by Django 3.2.4 on 2021-09-11 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('findTutor', '0021_parentmodel_subject_care'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parentmodel',
            name='subject_care',
        ),
        migrations.RemoveField(
            model_name='tutormodel',
            name='mon_day',
        ),
    ]
