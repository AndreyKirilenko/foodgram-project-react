# from django.contrib import admin
from django.urls import path, include
from django.urls.conf import include
from rest_framework import routers
from .views import (SubscriptionViewSet, UsersViewSet, SubscribeViewSet)

users_router = routers.DefaultRouter()

users_router.register(r'subscriptions', SubscriptionViewSet, basename='subscriptions')
users_router.register(r'(?P<id>[0-9]+)/subscribe', SubscribeViewSet, basename='subscribe')
users_router.register(r'', UsersViewSet, basename='users')

urlpatterns = [
    
    path('', include(users_router.urls)),
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