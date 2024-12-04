from http import HTTPStatus

from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView


# Create your views here.

class HomePage(TemplateView):
    template_name = 'common/index.html'
    pass

def ErrorView(request, **kwargs):
    code = kwargs.get('status_code',500)
    message = HTTPStatus(code).description
    context ={
        'code':code,
        'message':message
    }
    return render(request,'common/errors.html',context, status=code)