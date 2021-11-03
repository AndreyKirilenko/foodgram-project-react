from django.urls import include, path

from .views import ListUsersAPIView, CreateDeleteView

urlpatterns = [
    path('users/subscriptions/', ListUsersAPIView.as_view()),
    path('users/<int:id>/subscribe/', CreateDeleteView.as_view()),
    path('', include('djoser.urls')),
]