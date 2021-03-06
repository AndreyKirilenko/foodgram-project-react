from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


class CustomUser(AbstractUser):

    class UserRole(models.TextChoices):
        USER = USER
        MODERATOR = MODERATOR
        ADMIN = ADMIN

    username = models.CharField(null=False, unique=True, max_length=150)
    email = models.EmailField(null=False, unique=True, max_length=250)
    first_name = models.CharField(null=False, max_length=150)
    last_name = models.CharField(null=False, max_length=150)
    role = models.CharField(
        max_length=20, choices=UserRole.choices, default=UserRole.USER
    )

    def __str__(self):
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='follower'
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='following'
    )

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'], name='author_follows'
            ),
        ]
