

from django.utils.text import slugify


class ArticleUrl:

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        for article in queryset:
            print(slugify(article.title),article.title)
            article.article_url = self.request.build_absolute_uri() + f'{article.pk}/{article.title}/'
        return queryset