from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from izpitnik.orth_calendar.validators import RangeValidator


# Create your models here.

class Saint(models.Model):

    class Meta:
        verbose_name = _("saint")
        verbose_name_plural = _("saints")

    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name=_("name")
    )

    def __str__(self):
        return self.name



class Feast(models.Model):

    class Meta:
        verbose_name = _("feast")
        verbose_name_plural = _("feasts")

    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name = _("name")
    )
    # saint = models.ForeignKey(to=Saint, null=True, blank=True, related_name='feasts', on_delete=models.SET_NULL)
    saint = models.ManyToManyField(
        to=Saint,
        related_name='feasts',
        verbose_name=_("saint"),
        blank=True,
    )

    def __str__(self):
        return self.name


class HolidayOccurrences(models.Model):

    class CalendarChoices(models.TextChoices):
        JULIAN_IN_GREGORIAN = "JIG", _("Julian in gregorian")
        JULIAN = "J", _("Julian")
        GREGORIAN = "G", _("Gregorian")

    class Meta:
        verbose_name = _("holiday occurrence")
        verbose_name_plural = _("holiday occurrences")

    date = models.DateField(
        unique=True,
        verbose_name=_("date")
    )
    calendar = models.CharField(
        max_length=5,
        null=False,
        blank=True,
        default=CalendarChoices.JULIAN_IN_GREGORIAN,
        choices=CalendarChoices,
        verbose_name=_("calendar")
    )
    easter_distance = models.SmallIntegerField(
        validators=(RangeValidator(-365,365),),
        blank=True,
        null=True,
        editable=False,
        verbose_name=_("easter distance")
    )
    christmas_distance = models.SmallIntegerField(
        validators=(RangeValidator(1,365),),
            blank=True,
            null=True,
            editable=False,
            verbose_name=_("christmas distance")
    )
    feast = models.ManyToManyField(
        to=Feast,
        blank=True,
        related_name="occurrences",
        default=None,
        verbose_name=_("feast"),
    )
    saint = models.ManyToManyField(
        to=Saint,
        blank=True,
        related_name="occurrences",
        default=None,
        verbose_name=_("saint"),
    )

    def __str__(self):
        return f"{self.date.strftime("%Y. %m. %d.")} - {self.CalendarChoices._value2member_map_[self.calendar].name}"


class RelatedHolidayOccurrences(HolidayOccurrences):

    class Meta:
        proxy = True
        verbose_name = _("related holiday occurrence")
        verbose_name_plural = _("related holiday occurrences")


