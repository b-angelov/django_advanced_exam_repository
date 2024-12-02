from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def hstyle(objects, section, name, pattern="%s", params=None):
    result = ''
    params = params.split(',') if params else []
    section_obj = objects.filter(section_name=section).first()
    if section_obj:
        settings = section_obj.settings.filter(name=name,style=section_obj.section_style,enabled=True).first()
        if settings and settings.value:
            params = [hstyle(objects, section, param) for param in params]
            result = pattern % (settings.value if settings.value else '', *params)
    return mark_safe(result)