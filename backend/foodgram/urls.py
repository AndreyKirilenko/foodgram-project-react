from django.urls import path, include
from django.urls.conf import include
from rest_framework import routers
from .views import (Shopping_cartViewSet, FavoriteViewSet,
                    Quantity_ingredientsViewSet, RecipeViewSet, 
                    TagViewSet, IngredientsViewSet)

router = routers.DefaultRouter()

router.register(r'recipes/(?P<id>[0-9]+)/shopping_cart', Shopping_cartViewSet)
router.register(r'recipes/(?P<id>[0-9]+)/favorite', FavoriteViewSet, basename='favorite')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    
    path('', include(router.urls)),
]