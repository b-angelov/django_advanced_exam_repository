from re import search

from django import template
from pyunycode import pyunycode

register = template.Library()


@register.filter
def punytrans(value):
    return pyunycode.convert(search('(.[^:]+)',value)[0])
