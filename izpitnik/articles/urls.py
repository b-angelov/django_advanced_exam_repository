from django.urls import path, include

# from izpitnik.articles.api.views import ArticleLikeApiView
from izpitnik.articles.views import ArticleListView, ArticlesOnDate, ArticleView, ArticlesByUser, ArticleAddView, \
    ArticleDeleteView, ArticleEditView

urlpatterns = [
    # path('', ArticleListView.as_view()),
    path('', ArticleListView.as_view(), name='all-articles'),
    path('<int:pk>/', include([
        path('delete/', ArticleDeleteView.as_view(), name='article-delete'),
        path('edit/', ArticleEditView.as_view(), name='article-edit'),
        path('<str:title>/', ArticleView.as_view(), name='single-article'),
    ])),
    path('user_articles/', ArticlesByUser.as_view(), name='user-articles'),
    path('create/', ArticleAddView.as_view(), name='article-create'),
    path('<slug:date>/', ArticlesOnDate.as_view(), name='date-articles'),
]
