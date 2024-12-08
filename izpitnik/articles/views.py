from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from izpitnik.articles.forms import CreateArticleForm
from izpitnik.articles.mixins import ArticleUrl, article_url, NoDataMessage
from izpitnik.articles.models import Article
from izpitnik.orth_calendar.models import HolidayOccurrences


# Create your views here.

class ArticleListView(NoDataMessage, ArticleUrl, ListView):
    template_name = 'articles/articles.html'
    model = Article


class ArticlesByUser(ArticleListView):
    no_data_message = _('for this user')

    @article_url
    def get_queryset(self):
        return Article.objects.filter(author__pk=self.request.user.pk)




class ArticlesOnDate(ArticleListView):
    template_name = 'articles/articles.html'
    model = HolidayOccurrences
    no_data_message = _('for this day')

    def __init__(self, *args, **kwargs):
        self.date = datetime.today().date()
        if kwargs.get('date', None):
            self.date = datetime.strptime(kwargs.pop('date'),'%Y-%m-%d').date()
        super().__init__(*args, **kwargs)


    def get_queryset(self):
        date = self.date
        obj = self.model(date=date).object_by_date()
        return Article.objects.filter(Q(saint__in=obj.saint) | Q(feast__in=obj.feast))

class ArticleView(ArticleUrl,DetailView):
    model = Article
    template_name = 'articles/article.html'

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

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ArticleDeleteView(UserPassesTestMixin,DeleteView):
    model = Article
    template_name = 'articles/article-delete.html'

    def test_func(self):
        return self.object.author.pk == self.request.user.pk


