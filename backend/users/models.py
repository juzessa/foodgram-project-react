from django.contrib.auth.models import AbstractUser
from django.db import models

from recipes.constants import EMAIL, ONEHUNDREDFIFTY


class User(AbstractUser):
    email = models.EmailField(max_length=EMAIL)
    first_name = models.CharField(max_length=ONEHUNDREDFIFTY)
    last_name = models.CharField(max_length=ONEHUNDREDFIFTY)
    username = models.CharField(max_length=ONEHUNDREDFIFTY, unique=True)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique'
            ),
            models.CheckConstraint(
                name="recipes_follow_prevent_self_follow",
                check=~models.Q(author=models.F("user")),
            ),)

    def __str__(self):
        return self.name
