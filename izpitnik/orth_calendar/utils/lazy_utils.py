from django.utils.functional import lazy

def lstring(string):
    return string

def capitalize(string):
    return string.capitalize()

capitalize_lazy = lazy(capitalize, str)

get_lazy = lazy(lstring, str)