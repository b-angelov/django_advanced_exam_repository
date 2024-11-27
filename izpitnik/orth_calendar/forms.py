from datetime import timedelta, datetime

from django import forms
from django.contrib.admin.helpers import AdminForm
from django.db import models
from django.db.models import Q
from django.db.models.aggregates import Max
from django.forms.widgets import TextInput, Textarea
from django.utils.translation import gettext_lazy as _

from izpitnik.orth_calendar.models import Feast, Saint
from izpitnik.orth_calendar.utils.calculus import Calculus
from izpitnik.orth_calendar.utils.lazy_utils import capitalize_lazy


class HolidayOccurrencesAdminForm(forms.ModelForm):


    feast = forms.CharField(
        widget=forms.Textarea(attrs={"rows":10, "cols":35}),
        help_text = _("Add comma separated feast list here:"),
        required=False,
        label = capitalize_lazy(_("feast")),
    )

    saint = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 10, "cols": 35}),
        help_text=_("Add comma separated saints list here:"),
        required=False,
        label=capitalize_lazy(_("saint")),
    )

    def get_initial_for_field(self, field, field_name):
        initial = super().get_initial_for_field(field, field_name)
        if initial and field_name in ("feast","saint"):
            initial = ",\n".join(i.name for i in initial)
        if field_name == "date" and not initial:
            obj = self._meta.model
            initial = obj.objects.all().order_by("-date").first().date + timedelta(days=1)
        return initial or ''

    class Meta:
        widgets = {
            "feast":Textarea(),
            "saint":Textarea()
        }
        pass

    class Media:
        js = ('js/admin/add_style.js', )


    def clean_feast(self):
        feast_data = self.__parse_to_multiple(self.cleaned_data["feast"])
        feasts = []
        for feast in feast_data:
            feast, created = Feast.objects.get_or_create(name=feast)
            feasts.append(feast)
        return feasts

    def clean_saint(self):
        saint_data = self.__parse_to_multiple(self.cleaned_data["saint"])
        saints = []
        for saint in saint_data:
            saint, created = Saint.objects.get_or_create(name=saint)
            saints.append(saint)
        return saints

    @staticmethod
    def __parse_to_multiple(field, separator=","):
        field = field or ""
        return [field.strip() for field in field.split(separator)]

class RelatedHolidayOccurrencesAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial.get('date')
        self.fields['feast'].queryset = Feast.objects.filter(pk__in=self.__override_queryset('feast'))
        self.fields['saint'].queryset = Saint.objects.filter(pk__in=self.__override_queryset('saint'))

    # def get_initial_for_field(self, field, field_name):
    #     initial = super().get_initial_for_field(field,field_name)
    #     obj = self._meta.model
    #     if field_name in ('saint','feast'):
    #         date = self.initial.get('date')
    #         # date = datetime.strptime(date,'%Y-%m-%d')
    #         calendar = self.initial.get('calendar')
    #         print(self.initial.get('calendar'), date)
    #         distances = Calculus(date, calendar).get_distance()
    #         print(distances)
    #         initial = obj.objects.prefetch_related('saint','feast').filter(Q(easter_distance=distances['easter']) | Q(christmas_distance=distances['christmas']))
    #         if field_name == 'saint':
    #             initial = set(i for init in initial for i in init.saint.all())
    #             print(list(initial))
    #         elif field_name == 'feast':
    #             initial = set(i for init in initial for i in init.feast.all())
    #         initial = list(initial)
    #     return initial

    def get_initial_for_field(self, field, field_name):
        initial = super().get_initial_for_field(field, field_name)
        print(initial)
        if field_name == 'date' and not initial:
            initial = self._meta.model.objects.order_by('-pk').first().date + timedelta(days=1)
            print(initial)
        return initial

    def __override_queryset(self, field_name):
        initial = []
        obj = self._meta.model
        if field_name in ('saint', 'feast'):
            date = self.initial.get('date') or self.get_initial_for_field(self.fields['date'], 'date')
            # date = datetime.strptime(date,'%Y-%m-%d')
            calendar = self.initial.get('calendar') or 'JIG'
            print(self.initial.get('calendar'), date)
            distances = Calculus(date, calendar).get_distance()
            print(distances)
            initial = obj.objects.prefetch_related('saint', 'feast').filter(
                Q(easter_distance=distances['easter']) | Q(christmas_distance=distances['christmas']))
            if field_name == 'saint':
                initial = set(i.pk for init in initial for i in init.saint.all())
                print(list(initial))
            elif field_name == 'feast':
                initial = set(i.pk for init in initial for i in init.feast.all())
        return initial
