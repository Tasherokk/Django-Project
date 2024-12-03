# Generated by Django 5.1.3 on 2024-12-03 18:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0002_comment"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddIndex(
            model_name="comment",
            index=models.Index(
                fields=["course"], name="course_comm_course__57c831_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="comment",
            index=models.Index(
                fields=["author"], name="course_comm_author__76df4a_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="comment",
            index=models.Index(
                fields=["created_at"], name="course_comm_created_3f95b2_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="course",
            index=models.Index(
                fields=["created_at"], name="course_cour_created_49f06e_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="topic",
            index=models.Index(
                fields=["course"], name="course_topi_course__40f69e_idx"
            ),
        ),
    ]
