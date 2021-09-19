from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()



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
