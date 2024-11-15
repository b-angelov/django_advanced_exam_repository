from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from izpitnik.navigation.models import Navigation


# Create your views here.

class NavigationBarView(ListView):
    model = Navigation
    template_name = 'navigation/nav.html'

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.prefetch_related('children').filter(slug=self.kwargs['nav_name'])

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data["items"] = self.get_queryset()
        return context_data

