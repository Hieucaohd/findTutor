# Generated by Django 3.2.4 on 2021-10-09 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20211009_0846'),
    ]

    operations = [
        migrations.RenameField(
            model_name='linkmodel',
            old_name='link',
            new_name='url',
        ),
    ]
