# Generated by Django 3.2.4 on 2021-09-08 02:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('findTutor', '0017_alter_pricemodel_teacher'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pricemodel',
            old_name='money',
            new_name='money_per_day',
        ),
        migrations.RemoveField(
            model_name='pricemodel',
            name='time_price_pay_for',
        ),
    ]
