from django.contrib import admin
from . import models


@admin.register(models.Hackathon)
class HackathonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_datetime')


@admin.register(models.Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'submission_name', 'user', 'hackathon')


@admin.register(models.Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'hackathon')
