# Generated by Django 3.2.4 on 2021-08-30 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('findTutor', '0008_auto_20210830_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageofusermodel',
            name='image',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='oldimageprivateusermodel',
            name='image',
            field=models.TextField(),
        ),
    ]
