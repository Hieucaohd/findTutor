# Generated by Django 3.2.4 on 2021-09-08 02:44

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('findTutor', '0016_auto_20210906_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricemodel',
            name='teacher',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('sv', 'Sinh Vien'), ('gv', 'Giao Vien')], max_length=5),
        ),
    ]
