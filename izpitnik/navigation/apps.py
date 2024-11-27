from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NavigationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'izpitnik.navigation'
    verbose_name = _("navigation")
    verbose_name_plural = _("navigations")

