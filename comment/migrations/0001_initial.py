# Generated by Django 3.2.4 on 2021-08-12 03:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('findTutor', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentAboutTutorModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('about_who', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='findTutor.tutormodel')),
                ('belong_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='comment.commentabouttutormodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CommentAboutParentRoomModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('about_who', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='findTutor.parentroommodel')),
                ('belong_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='comment.commentaboutparentroommodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CommentAboutParentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('about_who', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='findTutor.parentmodel')),
                ('belong_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='comment.commentaboutparentmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
