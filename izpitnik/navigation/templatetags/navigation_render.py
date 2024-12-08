from django import template
from django.template.loader import render_to_string
from django.utils.translation import get_language

from izpitnik.navigation.models import Navigation, Menu

register = template.Library()


@register.simple_tag
def nav_render(template, slug, user):
    # items =  Navigation.objects.prefetch_related('children').filter(menu__slug=slug,language__icontains=get_language()).order_by("pk")
    menu,items = Menu.objects.filter(slug=slug).first().get_menu()
    uid = ''
    if not user.is_authenticated:
        items = items.filter(login_required=False)
    else:
        items = items.filter(anonymous_required=False)
        uid = f'?uid={user.pk}'
    items = filter(lambda item: not item.permission_required or user.has_perm(item.permission_required.codename), items )

    return render_to_string(template, {"items":items, 'uid':''})
