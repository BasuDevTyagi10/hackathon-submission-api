import os

from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User, Hackathon, Enrollment, Submission


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'is_staff']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']


class HackathonCreateSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    enrollments_count = serializers.SerializerMethodField()

    class Meta:
        model = Hackathon
        fields = ['title', 'description', 'background_image', 'hackathon_image',
                  'type_of_submission', 'start_datetime', 'end_datetime', 'reward_prize',
                  'created_by', 'enrollments_count']

    def get_enrollments_count(self, obj):
        try:
            return obj.enrollments.count()
        except AttributeError:
            return 0

    def validate_hackathon_image(self, value):
        image_extensions = ['.jpg', '.jpeg', '.png']
        ext = os.path.splitext(value.name)[1]
        if ext.lower() not in image_extensions:
            raise ValidationError(_("Hackathon image must be an image file."))
        return value

    def validate_background_image(self, value):
        image_extensions = ['.jpg', '.jpeg', '.png']
        ext = os.path.splitext(value.name)[1]
        if ext.lower() not in image_extensions:
            raise ValidationError(_("Background image must be an image file."))
        return value


class HackathonSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    enrollments_count = serializers.SerializerMethodField()

    class Meta:
        model = Hackathon
        fields = ['id', 'title', 'description', 'background_image', 'hackathon_image',
                  'type_of_submission', 'start_datetime', 'end_datetime', 'reward_prize',
                  'created_by', 'enrollments_count']

    def get_enrollments_count(self, obj):
        try:
            return obj.enrollments.count()
        except AttributeError:
            return 0


class EnrollmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    hackathon = HackathonSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'hackathon']
        read_only_fields = ['id']


class SubmissionCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    hackathon = HackathonSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = ['submission_name', 'summary', 'submission_file', 'submission_link', 'user', 'hackathon']
        

class SubmissionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    hackathon = HackathonSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'submission_name', 'summary', 'submission_file', 'submission_link', 'user', 'hackathon']
        read_only_fields = ['id', 'user', 'hackathon']
