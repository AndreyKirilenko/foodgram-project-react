from django.urls import include, path
from rest_framework import routers

from .views import ListUsersAPIView, CreateDeleteView




urlpatterns = [
    path('users/subscriptions/', ListUsersAPIView.as_view()),
    path('users/<id>/subscribe/', CreateDeleteView.as_view()),
    path('', include('djoser.urls')),
]