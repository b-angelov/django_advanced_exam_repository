from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OrthCalendarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'izpitnik.orth_calendar'
    verbose_name = _("orthodox calendar")
    verbose_name_plural = _("orthodox calendars")

