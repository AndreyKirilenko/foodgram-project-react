# from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
# User = get_user_model()
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):

    class UserRole(models.TextChoices):
        USER = 'USER', _('user')
        MODERATOR = 'MODERATOR', _('moderator')
        ADMIN = 'ADMIN', _('admin')

    username = models.CharField(null=False, unique=True, max_length=150)
    email = models.EmailField(null=False, max_length=250)
    first_name = models.CharField(null=False, max_length=150)
    last_name = models.CharField(null=False, max_length=150)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.USER)

    def __str__(self):
        return self.username




class Subscription(models.Model):  # Подписка
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='follower')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'], name='author_follows'
            ),
        ]