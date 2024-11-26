from django.contrib import admin

from .models import Course, Topic, Comment

# Register your models here.
admin.site.register(Course)
admin.site.register(Topic)
admin.site.register(Comment)