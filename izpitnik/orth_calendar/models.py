from datetime import datetime

from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from izpitnik.orth_calendar.managers import HolidaysRelatedManager
from izpitnik.orth_calendar.utils.calculus import Calculus
from izpitnik.orth_calendar.validators import RangeValidator
from calendar import monthrange


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

    objects = HolidaysRelatedManager()



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

    objects = HolidaysRelatedManager()



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
        verbose_name=_("feast")
    )

    saint = models.ManyToManyField(
        to=Saint,
        blank=True,
        related_name="occurrences",
        default=None,
        verbose_name=_("saint")
    )


    def __str__(self):
        return f"{self.date.strftime("%Y. %m. %d.")} - {self.CalendarChoices._value2member_map_[self.calendar].name}"


    def christmas_related_saints(self) -> QuerySet:
        return Saint.objects.get_christmas_related(str(self.date), calendar=self.calendar)

    def easter_related_saints(self) -> QuerySet:
        return Saint.objects.get_easter_related(str(self.date), calendar=self.calendar)

    def christmas_and_easter_related_saints(self) -> QuerySet:
        return Saint.objects.get_christmas_and_easter_related(str(self.date), calendar=self.calendar)

    def christmas_related_feasts(self) -> QuerySet:
        return Feast.objects.get_christmas_related(str(self.date), calendar=self.calendar)

    def easter_related_feasts(self) -> QuerySet:
        return Feast.objects.get_easter_related(str(self.date), calendar=self.calendar)

    def christmas_and_easter_related_feasts(self) -> QuerySet:
        return Feast.objects.get_christmas_and_easter_related(str(self.date), calendar=self.calendar)

    def christmas_and_easter_related_feasts_and_saints(self) -> dict:
        return {
            "saints":self.christmas_and_easter_related_saints(),
            "feasts":self.christmas_and_easter_related_feasts(),
        }

    def get_distance(self):
        return Calculus(date=datetime.strptime(str(self.date),'%Y-%m-%d').date(), calendar=self.calendar).get_distance()

    def object_by_date(self, date=None,calendar=None,committable=False):
        object = self.__class__(date=date or self.date,calendar=calendar or self.calendar)
        distance = object.get_distance()
        related = object.saints_and_feasts_of_the_day()
        object.easter_distance = distance['easter']
        object.christmas_distance = distance['christmas']
        if committable:
            object.save()
            object.feast.add(*related['feasts'])
            object.saint.add(*related['saints'])
            object.save()
            return object
        return MockedOccurrences(object,{'feast':related['feasts'],'saint':related['saints']})

    saints_and_feasts_of_the_day = christmas_and_easter_related_feasts_and_saints

    def get_saint(self):
        return self.saint or QuerySet()

    def get_feast(self):
        return self.feast or QuerySet()

    def get_holidays_for_this_month(self, date=None,calendar=None):
        date = date or self.date
        calendar = calendar or self.calendar
        date = date.replace(day=1)
        current_month_length = monthrange(date.year,date.month)[1]
        # object = self.__class__(date=date.date(), calendar=calendar)
        # distance = object.get_distance()
        # query_set = self.__class__.objects.filter(christmas_distance__in=range(distance["christmas"], distance["christmas"] + current_month_length)).distinct("christmas_distance")
        query_set = [None] * current_month_length
        def reset_date(_):
            nonlocal date
            res = self.__class__(date=date.date(), calendar=calendar).object_by_date()
            if date.day < current_month_length:
                date = date.replace(day=date.day+1)
            return res
        return list(map(reset_date, query_set))


class RelatedHolidayOccurrences(HolidayOccurrences):

    class Meta:
        proxy = True
        verbose_name = _("related holiday occurrence")
        verbose_name_plural = _("related holiday occurrences")

class MockedOccurrences():

    def __init__(self, instance, mocked_fields: dict):
        self.obj = instance
        for name,value in self.obj.__dict__.items():
            setattr(self, name, value)
        for name,value in mocked_fields.items():
            setattr(self, name, mocked_fields[name])
        self.mocked_fields = mocked_fields

    def save(self):
        self.obj.save()
        for field,value in self.mocked_fields.items():
            related_field = getattr(self.obj, field, None)
            if related_field and hasattr(related_field, 'add'):
                related_field.add(*value)
        self.obj.save()



