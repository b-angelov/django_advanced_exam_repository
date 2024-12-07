from django.contrib import admin
import unfold

from izpitnik.articles.models import Article


# Register your models here.


@admin.register(Article)
class ArticleAdmin(unfold.admin.ModelAdmin):
    pass
