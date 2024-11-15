from django import template
from django.template.loader import render_to_string

from izpitnik.navigation.models import Navigation

register = template.Library()


@register.simple_tag
def nav_render(template, slug):
    items =  Navigation.objects.prefetch_related('children').filter(slug=slug)
    return render_to_string(template, {"items":items})
