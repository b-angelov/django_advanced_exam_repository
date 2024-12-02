from django.db import models
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

# Create your models here.

SETTINGS_DEFAULT_STYLE = "marble"

class Section(models.Model):

    section_name = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        verbose_name=_("section name"),
    )
    section_style = models.CharField(
        max_length=20,
        default=SETTINGS_DEFAULT_STYLE,
        verbose_name=_("section style"),
    )

    def __str__(self):
        return self.section_name

    class Meta:
        verbose_name = _("section")
        verbose_name_plural = _("sections")

class Setting(models.Model):

    class TypeChoices(models.TextChoices):
        TEXT = "TXT", "Text"
        COLOR = "COL", "Colour"
        INTEGER = "INT", "Integer"
        URL = "URL", "URL"
        WHOLE_VALUE = "WV", "Whole Value"

    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name=_("name"),
    )
    value = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        default="",
        verbose_name=_("value"),
    )
    style = models.CharField(
        max_length=20,
        default=SETTINGS_DEFAULT_STYLE,
        verbose_name=_("style"),
    )
    type = models.CharField(
        max_length=15,
        choices=TypeChoices,
        default=TypeChoices.TEXT,
        null=False,
        blank=True,
        verbose_name=_("type"),
    )
    enabled = models.BooleanField(
        default=False,
        verbose_name = _("enabled"),
    )
    section = models.ForeignKey(
        to='Section',
        on_delete=models.CASCADE,
        related_name='settings',
        verbose_name = _("section"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("option")
        verbose_name_plural = _("settings")