# Generated by Django 5.1.1 on 2024-10-12 17:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0001_initial"),
        ("video", "0002_alter_video_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="video",
            name="topic",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="videos",
                to="course.topic",
            ),
        ),
    ]