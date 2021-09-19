from django.shortcuts import render

# from django.db.models import Avg
from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import PageNumberPagination
# from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

# from yamdb_auth.permissions import (IsAdminOrReadOnly,
#                                     IsAuthenticatedOrReadOnly,
#                                     IsAuthorAdminModeratorOrReadOnly)

# from .filters import TitleFilter
from .models import Subscription
# from .serializers import (CategorySerializer, CommentSerializer,
#                           GenreSerializer, ReviewSerializer, TitleSerializer,
#                           TitleSlugSerializer)

class UsersViewSet(viewsets.ModelViewSet):
    pass


class SubscriptionViewSet(viewsets.ModelViewSet):
    pass


class SubscribeViewSet(viewsets.ModelViewSet):
    pass