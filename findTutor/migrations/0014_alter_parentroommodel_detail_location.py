# Generated by Django 3.2.4 on 2021-09-01 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('findTutor', '0013_auto_20210831_0328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parentroommodel',
            name='detail_location',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
