# Generated by Django 3.2.4 on 2021-08-26 13:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('findTutor', '0002_auto_20210826_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageprivateusermodel',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
