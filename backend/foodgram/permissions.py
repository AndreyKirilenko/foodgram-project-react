import rest_framework.permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


# class IsAdminOrReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS:
#             return True
#         if request.user.is_authenticated:
#             return request.user.is_admin or request.user.is_superuser
#         else:
#             return False


# class IsAdmin(BasePermission):
#     def has_permission(self, request, view):
#         if request.user.is_authenticated:
#             return request.user.is_admin or request.user.is_superuser
#         else:
#             return False


# class IsModerator(BasePermission):
#     def has_permission(self, request, view):
#         if request.user.is_authenticated:
#             return request.user.is_moderator
#         else:
#             return False


class IsAuthenticatedOrReadOnly(BasePermission): # Нет смысла переопределять! Уже есть готовый!
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated


# IsAuthenticated = rest_framework.permissions.IsAuthenticated


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


# class IsModeratorOrReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS:
#             return True
#         return request.user.is_moderator


# class IsAuthorAdminModeratorOrReadOnly(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in SAFE_METHODS:
#             return True
#         if request.method == 'POST':
#             return request.user.is_authenticated
#         return request.user.is_authenticated and (
#             request.user == obj.author
#             or request.user.is_moderator
#             or request.user.is_admin
        # )
