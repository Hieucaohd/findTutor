# Generated by Django 3.2.4 on 2021-08-19 13:12

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('findTutor', '0003_auto_20210812_0346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parentroommodel',
            name='day_can_teach',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)], max_length=13),
        ),
    ]