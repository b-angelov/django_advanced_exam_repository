from django.utils import translation


def text_in_locale(text: str, locale: str):
    with translation.override(locale):
        return translation.gettext(text)