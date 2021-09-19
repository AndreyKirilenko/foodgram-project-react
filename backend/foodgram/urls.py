# from django.contrib import admin
from django.urls import path, include
from django.urls.conf import include
from rest_framework import routers
from .views import (Shopping_cartViewSet, FavoriteViewSet,
                    Quantity_ingredientsViewSet, RecipeViewSet, 
                    TagViewSet, IngredientsViewSet)

router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'recipes/(?P<id>[0-9]+)/favorite', FavoriteViewSet, basename='favorite')
router.register(r'recipes/download_shopping_cart', Shopping_cartViewSet, basename='shopping_cart')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    
    path('', include(router.urls)),
]



# v1_router = routers.DefaultRouter()
# v1_router.register(r'titles', TitleViewSet, basename='titles')
# v1_router.register(r'categories', CategoryViewSet, basename='categories')
# v1_router.register(r'genres', GenreViewSet, basename='genres')
# v1_router.register(
#     'titles/(?P<title_id>[0-9]+)/reviews',
#     ReviewViewSet,
#     basename='reviews'
# )
# v1_router.register(
#     'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
#     CommentViewSet,
#     basename='comments'
# )

# urlpatterns = [
#     path('v1/', include(v1_router.urls)),
#     path('v1/auth/', include('yamdb_auth.urls')),
#     path('v1/users/', include('users.urls')),
# ]