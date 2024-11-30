from datetime import datetime

from django.db import models
from django.db.models import Q, Count

from izpitnik.orth_calendar.decorators import set_calculus


class HolidaysRelatedManager(models.Manager):

    CALENDAR = 'JIG'

    @set_calculus(CALENDAR)
    def get_easter_related(self,date: datetime.date, distance_dict=None):
        if distance_dict.get('easter',None) is None:
            return self.filter(occurrences__easter_distance=None)
        queryset = self.filter(occurrences__easter_distance=distance_dict['easter'])
        return queryset.annotate(occ_count=Count('pk')).filter(occ_count__gt=1).distinct()

    @set_calculus(CALENDAR)
    def get_christmas_related(self, date: datetime.date, distance_dict=None):
        if distance_dict.get('christmas',None) is None:
            return self.filter(occurrences__christmas_distance=None)
        queryset = self.filter(occurrences__christmas_distance=distance_dict['christmas'])
        return queryset.annotate(occ_count=Count('pk')).filter(occ_count__gt=1).distinct()

    def get_christmas_and_easter_related(self,date:datetime.date):
        christmas_related = set(self.get_christmas_related(date).values_list(flat=True))
        easter_related = self.get_easter_related(date).values_list(flat=True)
        all = christmas_related.union(easter_related)
        return self.filter(pk__in=all)
