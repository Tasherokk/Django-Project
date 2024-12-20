# Generated by Django 5.1.1 on 2024-10-12 16:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0002_question_video"),
        ("video", "0002_alter_video_file"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="question",
            name="video",
        ),
        migrations.CreateModel(
            name="Test",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("questions", models.ManyToManyField(to="quiz.question")),
                (
                    "video",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="test",
                        to="video.video",
                    ),
                ),
            ],
        ),
    ]
