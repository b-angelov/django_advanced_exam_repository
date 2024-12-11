from datetime import datetime
from http.client import HTTPResponse

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import BadRequest
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from rest_framework.status import HTTP_400_BAD_REQUEST

from izpitnik.articles.forms import CreateArticleForm, EditArticleForm
from izpitnik.articles.mixins import ArticleUrl, article_url, NoDataMessage, SetOwnerAttribute, set_own_attribute
from izpitnik.articles.models import Article
from izpitnik.articles.permissions import IsAuthor
from izpitnik.orth_calendar.models import HolidayOccurrences


# Create your views here.

class ArticleListView(SetOwnerAttribute, NoDataMessage, ArticleUrl, ListView):
    template_name = 'articles/articles.html'
    model = Article


class ArticlesByUser(ArticleListView):
    no_data_message = _('for this user')

    @set_own_attribute
    @article_url
    def get_queryset(self):
        return Article.objects.filter(author__pk=self.request.user.pk)




class ArticlesOnDate(ArticleListView):
    template_name = 'articles/articles.html'
    model = HolidayOccurrences
    no_data_message = _('for this day')

    def __init__(self, *args, **kwargs):
        # self.date = datetime.today().date()
        # if kwargs.get('date', None):
        #     self.date = datetime.strptime(kwargs.pop('date'),'%Y-%m-%d').date()
        super().__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        try:
            self.date = datetime.today().date()
            if kwargs.get('date', None):
                self.date = datetime.strptime(kwargs.pop('date'),'%Y-%m-%d').date()
            return super().dispatch(request, *args, **kwargs)
        except ValueError:
            return HttpResponse('invalid date', status=404)

    def get_queryset(self):
        date = self.date
        obj = self.model(date=date).object_by_date()
        return Article.objects.filter(Q(saint__in=obj.saint) | Q(feast__in=obj.feast))

class ArticleView(ArticleUrl,DetailView):
    model = Article
    template_name = 'articles/article.html'

    @set_own_attribute
    def get_object(self, queryset = None):
        obj = super().get_object()
        return obj

    @set_own_attribute
    def get_queryset(self):
        pk = self.kwargs.get('pk',None)
        slug = self.kwargs.get('title', None)
        queryset = self.model.objects.filter(Q(pk=pk) | Q(title=slugify(slug)))
        return queryset

class ArticleAddView(LoginRequiredMixin,CreateView):
    template_name = 'articles/article-create.html'
    form_class = CreateArticleForm
    model = Article
    success_url = reverse_lazy('user-articles')
    login_url = reverse_lazy('login-page')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ArticleDeleteView(IsAuthor,UserPassesTestMixin,DeleteView):
    model = Article
    template_name = 'articles/article-delete.html'

    def get_success_url(self):
        return reverse_lazy('user-articles')

class ArticleEditView(IsAuthor,UpdateView):
    model = Article
    template_name = 'articles/article-edit.html'
    form_class = EditArticleForm

    def get_success_url(self):
        obj = self.get_object()
        print( obj.pk, obj.title)
        url = reverse_lazy('single-article', kwargs={"pk" : obj.pk, "title" : obj.title})
        return url




