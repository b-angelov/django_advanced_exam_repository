from django import template

register = template.Library()


@register.filter
def capitalize(value: str):
    return ' '.join(w.capitalize() for w in value.split())
