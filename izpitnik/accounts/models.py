from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from izpitnik.accounts.managers import UserManager


# Create your models here.


class User(AbstractUser):

    objects = UserManager()
    pass

class Profile(models.Model):

    user = models.OneToOneField(
        to=get_user_model(),
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        unique=True,
    )

    description = models.TextField(
        max_length = 3000,
        null=True,
        blank=True,
    )

    image = models.ImageField(
        null=True,
        blank=True,
        default='images/accounts/profile.png'
    )

    birth_date = models.DateField(
        null=True,
        blank=True,
    )

    @property
    def age(self):
        if self.birth_date:
            return int((date.today() - self.birth_date).days // 365.25)

    def __str__(self):
        return self.user.username

