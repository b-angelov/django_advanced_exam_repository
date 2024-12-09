from django import forms

from izpitnik.articles.models import Article


class CreateArticleForm(forms.ModelForm):

    class Meta:
        exclude = ['pk', 'author', 'holiday']
        model = Article


class EditArticleForm(CreateArticleForm):
    pass

