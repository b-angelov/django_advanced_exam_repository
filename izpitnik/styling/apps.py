from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StylingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'izpitnik.styling'
    verbose_name = _("styling")
    verbose_name_plural = _("stylings")
