from http import HTTPStatus

from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from izpitnik.articles.views import ArticlesOnDate


# Create your views here.

class HomePage(TemplateView):
    template_name = 'common/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles_today = ArticlesOnDate.as_view()(self.request).context_data["object_list"]
        context['articles'] = articles_today
        return context


def ErrorView(request, **kwargs):
    code = kwargs.get('status_code',500)
    message = HTTPStatus(code).description
    context ={
        'code':code,
        'message':message
    }
    return render(request,'common/errors.html',context, status=code)