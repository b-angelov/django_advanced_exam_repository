from django import template

register = template.Library()

@register.filter
def capitalize():
    pass

