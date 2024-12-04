# Generated by Django 5.1.3 on 2024-12-04 03:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quiz', '0004_answer_quiz_answer_correct_210c93_idx_and_more'),
        ('video', '0003_video_topic'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TestAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_attempts', to='quiz.test')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_attempts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [models.Index(fields=['user'], name='analytics_t_user_id_5a0b4e_idx'), models.Index(fields=['test'], name='analytics_t_test_id_7553f7_idx'), models.Index(fields=['timestamp'], name='analytics_t_timesta_46cb31_idx')],
            },
        ),
        migrations.CreateModel(
            name='VideoView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_views', to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_views', to='video.video')),
            ],
            options={
                'indexes': [models.Index(fields=['user'], name='analytics_v_user_id_eea2b8_idx'), models.Index(fields=['video'], name='analytics_v_video_i_283e74_idx'), models.Index(fields=['timestamp'], name='analytics_v_timesta_bb4187_idx')],
            },
        ),
    ]
