from django import template
from django.template.loader import render_to_string
from django.utils.translation import get_language

from izpitnik.navigation.models import Navigation, Menu

register = template.Library()


@register.simple_tag
def nav_render(template, slug):
    # items =  Navigation.objects.prefetch_related('children').filter(menu__slug=slug,language__icontains=get_language()).order_by("pk")
    menu,items = Menu.objects.filter(slug=slug).first().get_menu()
    return render_to_string(template, {"items":items})
