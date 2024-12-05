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


