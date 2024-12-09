from django.db.models import QuerySet
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify


class ArticleUrl:

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        self.set_urls(queryset)
        return queryset

    def set_url(self, article):
        article.article_url = reverse('single-article', args=(article.pk, article.title))# + f'/{article.pk}/{article.title}/'
        return article

    def set_urls(self, articles: QuerySet):
        for article in articles:
            self.set_url(article)
        return articles

class NoDataMessage:

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        if hasattr(self, 'no_data_message'):
            context['for_this_day'] = self.no_data_message
        return context

class SetOwnerAttribute:

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = self.set_is_own(self, queryset)
        return queryset

    @classmethod
    def set_is_own(cls,instance, queryset):
        if not hasattr(queryset, '__iter__'):
            queryset.is_own = (instance.request.user.pk == queryset.author.pk) or instance.request.user.is_superuser
            return queryset
        for article in queryset:
            article.is_own = (instance.request.user.pk == article.author.pk) or instance.request.user.is_superuser
        return queryset




def article_url(func):
    def wrapper(self):
        arturl = ArticleUrl()
        res = func(self)
        arturl.set_urls(res)
        return res
    return wrapper

def set_own_attribute(func):
    def wrapper(self):
        queryset = func(self)
        queryset = SetOwnerAttribute.set_is_own(self, queryset)
        return queryset
    return wrapper
