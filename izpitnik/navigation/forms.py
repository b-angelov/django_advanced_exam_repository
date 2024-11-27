from django import forms
from django.utils.translation import gettext_lazy as _, get_language

from izpitnik.orth_calendar.utils.lazy_utils import get_lazy
from utils.locale_utils import text_in_locale


class NavigationLanguageForm(forms.ModelForm):

    name = forms.CharField(
        disabled=True,
        label=_("name")
    )

    language_code = forms.CharField(
        disabled=True,
        label=_("language code")
    )

