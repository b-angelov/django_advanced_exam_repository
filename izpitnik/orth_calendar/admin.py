import unfold
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from izpitnik.orth_calendar.forms import HolidayOccurrencesAdminForm, RelatedHolidayOccurrencesAdminForm
from izpitnik.orth_calendar.models import HolidayOccurrences, Feast, Saint, RelatedHolidayOccurrences
from izpitnik.orth_calendar.utils.calculus import Calculus


# Register your models here.

@admin.register(HolidayOccurrences)
class HolidayOccurrencesAdmin(unfold.admin.ModelAdmin):
    form = HolidayOccurrencesAdminForm

    def save_model(self, request, obj, form, change):
        feasts = form.cleaned_data["feast"]
        saints = form.cleaned_data["saint"]
        calculus = Calculus(form.cleaned_data["date"],form.cleaned_data["calendar"])
        obj.easter_distance = self.__get_distance("easter_distance",calculus.easter_distance,form.cleaned_data)
        obj.christmas_distance = self.__get_distance("christmas_distance",calculus.christmas_distance,form.cleaned_data)
        obj.save()
        obj.feast.set(feasts)
        obj.saint.set(saints)


    @staticmethod
    def __get_distance(field, method, cleaned_data):
        distance_data = cleaned_data.get(field, None)
        if not distance_data:
            distance_data = method()
        return distance_data

@admin.register(RelatedHolidayOccurrences)
class HolidayOccurencesRelatedAdmin(unfold.admin.ModelAdmin):

    form = RelatedHolidayOccurrencesAdminForm



@admin.register(Feast)
class FeastAdmin(unfold.admin.ModelAdmin):
    pass

@admin.register(Saint)
class SaintAdmin(unfold.admin.ModelAdmin):
    pass


