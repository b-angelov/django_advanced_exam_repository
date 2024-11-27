from django.shortcuts import render
from django.utils.translation import get_language
from django.views.generic import TemplateView, ListView

from izpitnik.navigation.models import Navigation


# Create your views here.

class NavigationBarView(ListView):
    model = Navigation
    template_name = 'navigation/nav.html'

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.prefetch_related('children').filter(menu__slug=self.kwargs['nav_name'],language__icontains=get_language()).order_by("pk")

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data["items"] = self.get_queryset()
        return context_data

