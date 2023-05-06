from django.db import models
from django.contrib.auth.models import User

from utils.abstract_model import AbstractModel


class Hackathon(AbstractModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    background_image = models.ImageField(upload_to='hackathon_backgrounds/')
    hackathon_image = models.ImageField(upload_to='hackathon_images/')
    TYPE_CHOICES = [
        ('image', 'Image'),
        ('file', 'File'),
        ('link', 'Link')
    ]
    type_of_submission = models.CharField(max_length=5, choices=TYPE_CHOICES)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    reward_prize = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hackathons_created')

    def __str__(self):
        return str(self.title) + " - " + str(self.start_datetime)


class Enrollment(AbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='enrollments')

    def __str__(self):
        return str(self.user) + " - " + str(self.hackathon)


class Submission(AbstractModel):
    submission_name = models.CharField(max_length=255)
    summary = models.TextField()
    submission_file = models.FileField(upload_to='hackathon_submissions/', null=True)
    submission_link = models.URLField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='submissions')

    def __str__(self):
        return str(self.submission_name) + " - " + str(self.user)
