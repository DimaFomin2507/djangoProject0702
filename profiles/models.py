from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Profiles(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Пространство',
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class ProfilesRole(models.Model):
    profiles = models.ForeignKey(
        Profiles,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

