import os
from rest_framework import views
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from .models import Hackathon, Enrollment, Submission
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    HackathonSerializer,
    HackathonCreateSerializer,
    EnrollmentSerializer,
    SubmissionCreateSerializer,
    SubmissionSerializer,
)


class HomeAPIView(views.APIView):
    def get(self, request):
        return Response({'status': 'Submission API is running.'})


class UserCreateAPIView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_data = serializer.data
            user = User.objects.create_user(username=user_data['username'], password=user_data['password'])

            user.email = user_data.get('email', '')
            user.first_name = user_data.get('first_name', '')
            user.last_name = user_data.get('last_name', '')
            user.is_staff = user_data.get('is_staff', False)

            user.save()

            response = UserSerializer(user)
            return Response(response.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveAPIView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        requested_user = None
        try:
            if username is not None:
                requested_user = User.objects.get(username=username)
        except User.DoesNotExist:
            response_data = {
                "error": f"Requested user with username '{username}' does not exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(requested_user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserEnrolledHackathonsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        requested_user = None
        try:
            if username is not None:
                requested_user = User.objects.get(username=username)
        except User.DoesNotExist:
            response_data = {
                "error": f"Requested user with username '{username}' does not exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        enrollments = Enrollment.objects.filter(user=requested_user)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserEnrolledHackathonSubmissionAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        hackathon_id = kwargs.get('hackathon_id')
        submission_id = kwargs.get('submission_id')
        requested_submission = None
        try:
            if username is not None:
                User.objects.get(username=username)
            if hackathon_id is not None:
                Hackathon.objects.get(pk=hackathon_id)
            if submission_id is not None:
                requested_submission = Submission.objects.get(pk=submission_id)
        except User.DoesNotExist:
            response_data = {
                "error": f"Requested user with username '{username}' does not exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Hackathon.DoesNotExist:
            response_data = {
                "error": f"Requested hackathon with id '{hackathon_id}' does not exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Submission.DoesNotExist:
            response_data = {
                "error": f"Requested submission with id '{submission_id}' does not exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as error:
            response_data = {
                "error": str(error)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
       
        serializer = SubmissionSerializer(requested_submission)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserEnrolledHackathonSubmissionsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        requested_user = None
        try:
            if username is not None:
                requested_user = User.objects.get(username=username)
        except User.DoesNotExist:
            response_data = {
                "error": f"Requested user with key '{username}' does not exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        submissions = Submission.objects.filter(user=requested_user)
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EnrolledUserListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            enrolled_users_id = Enrollment.objects.values_list('user', flat=True).distinct()
            users = get_user_model().objects.filter(id__in=enrolled_users_id)
            serialized_data = UserSerializer(users, many=True).data
            return Response(serialized_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'You are not authorized to view this resource.'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class UnenrolledUserListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            enrolled_users_id = Enrollment.objects.values_list('user', flat=True).distinct()
            users = get_user_model().objects.exclude(id__in=enrolled_users_id)
            serialized_data = UserSerializer(users, many=True).data
            return Response(serialized_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'You are not authorized to view this resource.'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class HackathonCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            serializer = HackathonCreateSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                instance = serializer.save(created_by=self.request.user)
                serialized_data = HackathonSerializer(instance).data
                return Response(serialized_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'error': 'You are not authorized to create a hackathon.'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class HackathonRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        hackathon_id = kwargs.get('id')
        requested_hackathon = None
        try:
            if hackathon_id is not None:
                requested_hackathon = Hackathon.objects.get(id=hackathon_id)
        except Hackathon.DoesNotExist:
            response_data = {
                "error": f"Requested hackathon with id '{hackathon_id}' does not exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = HackathonSerializer(requested_hackathon)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HackathonRegisterAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        hackathon_id = kwargs.get('id')
        requested_hackathon = None
        try:
            if hackathon_id is not None:
                requested_hackathon = Hackathon.objects.get(id=hackathon_id)
        except Hackathon.DoesNotExist:
            response_data = {
                "error": f"Requested hackathon with id '{hackathon_id}' does not exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        enrollment = Enrollment(user=request.user, hackathon=requested_hackathon)
        enrollment.save()
        return Response({'status': 'Enrolled successfully'}, status=status.HTTP_201_CREATED)


class HackathonSubmissionAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        hackathon_id = kwargs.get('id')
        requested_hackathon = None
        try:
            if hackathon_id is not None:
                requested_hackathon = Hackathon.objects.get(id=hackathon_id)
        except Hackathon.DoesNotExist:
            response_data = {
                "error": f"Requested hackathon with id '{hackathon_id}' does not exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = SubmissionCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            instance = None
            if requested_hackathon.type_of_submission == 'link':
                if 'submission_link' in data and data['submission_link']:
                    instance = serializer.save(
                        user=self.request.user,
                        hackathon=requested_hackathon,
                        submission_link=data['submission_link'])
                else:
                    return Response(
                        {'error': "This hackathon accepts 'link' as type of submission. "
                                  "Please provide a valid link in the request body using 'submission_link' key."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            elif requested_hackathon.type_of_submission in ['image', 'file']:
                if 'submission_file' in data and data['submission_file']:
                    if requested_hackathon.type_of_submission == 'image':
                        image_extensions = ['.jpg', '.jpeg', '.png']
                        ext = os.path.splitext(data['submission_file'])[1]
                        if ext.lower() not in image_extensions:
                            return Response(
                                {'error': "Upload a valid image. "
                                          "The file you uploaded was either not an image or a corrupted image."},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                    instance = serializer.save(
                        user=self.request.user,
                        hackathon=requested_hackathon,
                        submission_file=data['submission_file']
                    )
                else:
                    return Response(
                        {'error': f"This hackathon accepts '{requested_hackathon.type_of_submission}' "
                                  f"as type of submission. "
                                  f"Please provide a valid file in the request body using 'submission_file' key."},
                        status=status.HTTP_400_BAD_REQUEST)
            serialized_data = SubmissionSerializer(instance).data
            return Response(serialized_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HackathonSubmissionsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        hackathon_id = kwargs.get('id')
        requested_hackathon = None
        try:
            if hackathon_id is not None:
                requested_hackathon = Hackathon.objects.get(id=hackathon_id)
        except Hackathon.DoesNotExist:
            response_data = {
                "error": f"Requested hackathon with id '{hackathon_id}' does not exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        if self.request.user.is_authenticated and self.request.user.is_staff:
            submissions = Submission.objects.filter(hackathon=requested_hackathon)
            serializer = SubmissionSerializer(submissions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'You are not authorized to view the hackathon submissions.'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class HackathonListAPIView(generics.ListAPIView):
    queryset = Hackathon.objects.all()
    serializer_class = HackathonSerializer
