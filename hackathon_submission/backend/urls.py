from django.urls import path
from .views import (
    HomeAPIView,
    UserCreateAPIView,
    UserRetrieveAPIView,
    UserEnrolledHackathonsAPIView,
    UserEnrolledHackathonSubmissionAPIView,
    UserEnrolledHackathonSubmissionsAPIView,
    UserListAPIView,
    EnrolledUserListAPIView,
    UnenrolledUserListAPIView,
    HackathonCreateAPIView,
    HackathonRetrieveAPIView,
    HackathonRegisterAPIView,
    HackathonSubmissionAPIView,
    HackathonSubmissionsAPIView,
    HackathonListAPIView,
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', HomeAPIView.as_view(), name='home'),

    path('auth-token', obtain_auth_token),
    
    path('user', UserCreateAPIView.as_view(), name='user-create'),
    path('user/<str:username>/', UserRetrieveAPIView.as_view(), name='user-retrieve'),
    path('user/<str:username>/hackathons/', UserEnrolledHackathonsAPIView.as_view(), name='user-enrolled-hackathons'),
    path('user/<str:username>/hackathon/<str:hackathon_id>/submission/<str:submission_id>', UserEnrolledHackathonSubmissionAPIView.as_view(), name='user-enrolled-hackathon-submissions'),
    path('user/<str:username>/hackathons/submissions/', UserEnrolledHackathonSubmissionsAPIView.as_view(), name='user-enrolled-hackathons-submissions'),
    path('users/', UserListAPIView.as_view(), name='user-list'),

    path('enrolled-users/', EnrolledUserListAPIView.as_view(), name='enrolled-user-list'),
    path('unenrolled-users/', UnenrolledUserListAPIView.as_view(), name='unenrolled-user-list'),
    
    path('hackathon', HackathonCreateAPIView.as_view(), name='hackathon-create'),
    path('hackathon/<str:id>/', HackathonRetrieveAPIView.as_view(), name='hackathon-retrieve'),
    path('hackathon/<str:id>/register', HackathonRegisterAPIView.as_view(), name='hackathon-register'),
    path('hackathon/<str:id>/submission', HackathonSubmissionAPIView.as_view(), name='hackathon-submission'),
    path('hackathon/<str:id>/submissions', HackathonSubmissionsAPIView.as_view(), name='hackathon-submissions'),
    path('hackathons/', HackathonListAPIView.as_view(), name='hackathon-list'),
]
