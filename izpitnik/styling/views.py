from django.shortcuts import render
from django.views.generic import ListView

from izpitnik.styling.models import Section


# Create your views here.

class DynamicStyleView(ListView):
    template_name = 'styling/css/dstyles.css'
    model = Section
    content_type = 'text/css'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(section_style=self.kwargs['style_name'])

class DynamicJSView(DynamicStyleView):

    template_name = 'styling/js/dstyle.js'
    content_type = 'text/javascript'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(section_style=self.kwargs['style_name'])
