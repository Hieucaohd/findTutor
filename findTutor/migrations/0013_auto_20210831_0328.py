# Generated by Django 3.2.4 on 2021-08-31 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('findTutor', '0012_alter_imageofusermodel_type_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageofusermodel',
            name='image',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='imageofusermodel',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='imageofusermodel',
            name='type_image',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
