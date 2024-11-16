from django.db import models
from django.db.models import TextChoices

# Create your models here.

SETTINGS_DEFAULT_STYLE = "marble"

class Section(models.Model):

    section_name = models.CharField(max_length=30, null=False,blank=False)
    section_style = models.CharField(max_length=20, default=SETTINGS_DEFAULT_STYLE)

    def __str__(self):
        return self.section_name

class Setting(models.Model):

    class TypeChoices(models.TextChoices):
        TEXT = "TXT", "Text"
        COLOR = "COL", "Colour"
        INTEGER = "INT", "Integer"
        URL = "URL", "URL"
        WHOLE_VALUE = "WV", "Whole Value"

    name = models.CharField(max_length=50, null=False, blank=False)
    value = models.CharField(max_length=50, null=True, blank=True, default="")
    style = models.CharField(max_length=20, default=SETTINGS_DEFAULT_STYLE)
    type = models.CharField(max_length=15, choices=TypeChoices, default=TypeChoices.TEXT, null=False, blank=True)
    enabled = models.BooleanField(default=True)
    section = models.ForeignKey(to='Section', on_delete=models.CASCADE, related_name='settings')

    def __str__(self):
        return self.name