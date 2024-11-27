from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.functional import lazy
from django.utils.translation import gettext_lazy as _, get_language
from prompt_toolkit.validation import ValidationError

from izpitnik.orth_calendar.utils.lazy_utils import get_lazy
from izpitnik.settings import LANGUAGES
from utils.locale_utils import text_in_locale


# Create your models here.

class Menu(models.Model):

    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name=_("name")
    )

    slug = models.SlugField(
        max_length=50,
        blank=True,
        null=False,
        verbose_name=_("slug"),
        unique=True,
    )

    class Meta:
        verbose_name = _("menu")
        verbose_name_plural = _("menus")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = '-'.join(c for c in self.name.lower().split())
        return super().save(*args,**kwargs)

    def get_menu(self):
        menu = self.__class__.objects.prefetch_related("navigation").filter(name=self.name,slug=self.slug).first()
        navigation = menu.navigation.prefetch_related("children").filter(language__language_code__icontains=get_language()).order_by("order","pk")
        return menu,navigation


class Navigation(models.Model):

    menu = models.ManyToManyField(
        to=Menu,
        blank=True,
        related_name="navigation"
    )

    item_name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name=_("item name")
    )
    url_external = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("external URL")
    )
    url_internal = models.SlugField(
        blank=True,
        null=True,
        verbose_name=_("internal URL")
    )
    parent_id = models.ForeignKey(
        to='Navigation',
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.SET(-1),
        verbose_name=_("parent ID")
    )

    # language = models.CharField(
    #     max_length=7,
    #     choices=LANGUAGES,
    #     default="en",
    #     verbose_name=_("language"),
    # )

    language = models.ManyToManyField(
        to="Language",
        blank=True,
        verbose_name=_("language"),
    )

    order = models.SmallIntegerField(
        null=False,
        blank=True,
        default=0,
        verbose_name=_("order")
    )

    def save(self, *args, **kwargs):
        if Language.objects.count() != len(LANGUAGES):
            for language in LANGUAGES:
                Language.objects.get_or_create(name=text_in_locale(language[1],"en"),language_code=language[0])
        if not self.order:
            self.order = self.__class__.objects.filter(menu__name=self.menu.first(),language__name=self.language).count() + 1
        return super().save(*args,**kwargs)

    class Meta:
        unique_together = ('url_external', 'url_internal')
        verbose_name = _("navigation")
        verbose_name_plural = _("navigations")

    def __str__(self):
        return self.item_name

    def resolved_url(self):
        try:
            url = self.url_internal
            if url:
                url = reverse(self.url_internal)
        except:
            url = self.url_external
        return url


class Language(models.Model):

    name = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        verbose_name=_("name")
    )

    language_code = models.CharField(
        max_length=8,
        null=False,
        blank=True,
        verbose_name=_("language code")
    )

    class Meta:
        verbose_name = _("language")
        verbose_name_plural=_("languages")

    def __str__(self):
        return self.name
