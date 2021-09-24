from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
User = get_user_model()


# USER = 'user'
# MODERATOR = 'moderator'
# ADMIN = 'admin'


# class ConfirmationCode(models.Model):

#     email = models.EmailField(null=False, unique=True)
#     confirmation_code = models.CharField(
#         max_length=20,
#         blank=True,
#         editable=False,
#         null=True,
#         unique=True)


class CustomUser(AbstractUser):
    pass
    # class UserRole(models.TextChoices):
    #     USER = USER
    #     MODERATOR = MODERATOR
    #     ADMIN = ADMIN

    # email = models.EmailField(null=False, unique=True)
    # first_name = models.CharField(null=True, max_length=30)
    # last_name = models.CharField(null=True, max_length=30)
    # role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.USER)


class Subscription(models.Model):  # Подписка
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'], name='author_follows'
            ),
        ]
