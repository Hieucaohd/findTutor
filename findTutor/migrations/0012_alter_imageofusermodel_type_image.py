# Generated by Django 3.2.4 on 2021-08-31 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('findTutor', '0011_imageofusermodel_is_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageofusermodel',
            name='type_image',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]