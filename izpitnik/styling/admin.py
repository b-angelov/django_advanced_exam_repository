import unfold
from colorfield.fields import ColorField
from django import forms
from django.contrib import admin
from django.db.models import CharField
from django.template.loader import render_to_string
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from izpitnik.styling.forms import SettingsChangelistForm
from izpitnik.styling.models import Section, Setting


# Register your models here.


@admin.register(Section)
class SectionAdmin(unfold.admin.ModelAdmin):
    list_display = ['section_name', 'section_style']

@admin.register(Setting)
class SettingAdmin(unfold.admin.ModelAdmin):
    list_display = ['name','value','enabled','section','type']
    list_editable = ['enabled','value','type']
    list_filter = ['style','section']



    # @admin.display(description=_("value"))
    # def cust_value(self, obj):
    #     if obj.type.lower() == "col":
    #         return format_html("<input type='color' value='{}' name='cust_value'>", obj.value)
    #     return format_html("<input type='text' value='{}' name='cust_value'>", obj.value)

    def get_changelist_form(self, request, **kwargs):
        kwargs["form"] = SettingsChangelistForm
        return super().get_changelist_form(request,**kwargs)

