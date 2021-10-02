from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import PageNumberPagination
# from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

# from yamdb_auth.permissions import (IsAdminOrReadOnly,
#                                     IsAuthenticatedOrReadOnly,
#                                     IsAuthorAdminModeratorOrReadOnly)

# from .filters import TitleFilter
from .models import Ingredients, Tag, Recipe, Quantity_ingredients, Favorite, Shopping_cart
from .serializers import (RecipeSerializer, Shopping_cartSerializer, )



class Shopping_cartViewSet(viewsets.ModelViewSet):
    serializer_class = Shopping_cartSerializer
    queryset = Shopping_cart.objects.all()


class FavoriteViewSet(viewsets.ModelViewSet):
    pass


class Quantity_ingredientsViewSet(viewsets.ModelViewSet):
    pass


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'tags']


class TagViewSet(viewsets.ModelViewSet):
    pass


class IngredientsViewSet(viewsets.ModelViewSet):
    pass