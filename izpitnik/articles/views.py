from datetime import datetime

from django.db.models import Q
from django.shortcuts import render
from django.utils.text import slugify
from django.views.generic import ListView, DetailView

from izpitnik.articles.mixins import ArticleUrl
from izpitnik.articles.models import Article
from izpitnik.orth_calendar.models import HolidayOccurrences


# Create your views here.

class ArticleListView(ArticleUrl, ListView):
    template_name = 'articles/articles.html'
    model = Article

class ArticlesOnDate(ArticleUrl,ListView):
    template_name = 'articles/articles.html'
    model = HolidayOccurrences

    def __init__(self, *args, **kwargs):
        self.date = datetime.today().date()
        if kwargs.get('date', None):
            self.date = datetime.strptime(kwargs.pop('date'),'%Y-%m-%d').date()
        print(args,kwargs)
        super().__init__(*args, **kwargs)
        print(self.date)


    def get_queryset(self):
        date = self.date
        obj = self.model(date=date).object_by_date()
        return Article.objects.filter(Q(saint__in=obj.saint) | Q(feast__in=obj.feast))

class ArticleView(DetailView):
    model = Article
    template_name = 'articles/article.html'

    def get_queryset(self):
        pk = self.kwargs.get('pk',None)
        slug = self.kwargs.get('title', None)
        queryset = self.model.objects.filter(Q(pk=pk) | Q(title=slugify(slug)))
        return queryset

