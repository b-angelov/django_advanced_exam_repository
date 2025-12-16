from django.db import models

from izpitnik.accounts.models import User
from izpitnik.orth_calendar.models import Saint, Feast, HolidayOccurrences


# Create your models here.

class Article(models.Model):

    title = models.CharField(
        max_length = 1000,
        blank=False,
        null=False
    )

    content = models.TextField(
        blank=True,
        null=True
    )

    image =models.ImageField(
        null=True,
        blank=True,
        default=None
    )

    saint = models.ManyToManyField(
        to=Saint,
        blank=True
    )

    feast = models.ManyToManyField(
        to=Feast,
        blank=True
    )

    holiday = models.ManyToManyField(
        to=HolidayOccurrences,
        blank=True
    )

    author = models.ForeignKey(
        to=User,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

class Comment(models.Model):

    title = models.CharField(
        blank=True,
        null=True,
        max_length=100
    )

    content = models.TextField(
        blank=False,
        null=True,
    )

    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=False,
        blank=True,
    )

    article = models.ForeignKey(
        to = Article,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title

class Likes(models.Model):

    user = models.ForeignKey(
        to=User,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

    article = models.ForeignKey(
        to=Article,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.user.username} likes {self.article.title}"
