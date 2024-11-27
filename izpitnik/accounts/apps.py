from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'izpitnik.accounts'
    verbose_name = _("account")
    verbose_name_plural = _("accounts")

