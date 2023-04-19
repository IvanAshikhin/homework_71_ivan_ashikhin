from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import UserManager

SEX = (('Male', 'male'),
       ('Female', 'female'),
       )


class Account(AbstractUser):
    email = models.EmailField(verbose_name='Электронная почта', unique=True, blank=True)
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to='avatars',
        verbose_name='Аватар',
        default='avatars/Default.jpg'
    )
    user_info = models.TextField(
        max_length=3000,
        verbose_name='Описание',
        null=True)
    sex = models.CharField(max_length=200, null=False, verbose_name='Пол', choices=SEX)
    phone = models.CharField(max_length=20)
    liked_posts = models.ManyToManyField(
        verbose_name='Понравившиеся публикации',
        to='posts.Post',
        related_name='user_likes')
    subscriptions = models.ManyToManyField(
        verbose_name='Подписки',
        to='accounts.Account',
        related_name='subscribers')
    commented_posts = models.ManyToManyField(
        verbose_name='Прокомментированные публикации',
        to='posts.Post',
        related_name='user_comments'
    ),

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    object = UserManager()

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
