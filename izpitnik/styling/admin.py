from django.contrib import admin

from izpitnik.styling.models import Section, Setting


# Register your models here.


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['section_name', 'section_style']

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ['name','value','enabled','section']
    list_editable = ['value','enabled']
