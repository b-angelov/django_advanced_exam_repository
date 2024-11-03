from django.contrib.auth.models import AbstractUser
from django.db import models

from izpitnik.accounts.managers import UserManager


# Create your models here.


class User(AbstractUser):

    objects = UserManager()
    pass

