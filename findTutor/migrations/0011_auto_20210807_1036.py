# Generated by Django 3.2.4 on 2021-08-07 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('findTutor', '0010_delete_commentabouttutormodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notifiedparentmodel',
            name='notifiedmodel_ptr',
        ),
        migrations.RemoveField(
            model_name='notifiedparentmodel',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='notifiedtutormodel',
            name='notifiedmodel_ptr',
        ),
        migrations.RemoveField(
            model_name='notifiedtutormodel',
            name='tutor',
        ),
        migrations.DeleteModel(
            name='NotifiedModel',
        ),
        migrations.DeleteModel(
            name='NotifiedParentModel',
        ),
        migrations.DeleteModel(
            name='NotifiedTutorModel',
        ),
    ]
