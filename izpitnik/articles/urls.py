from django.urls import path, include

from izpitnik.articles.views import ArticleListView, ArticlesOnDate, ArticleView, ArticlesByUser, ArticleAddView, \
    ArticleDeleteView

urlpatterns = [
    # path('', ArticleListView.as_view()),
    path('', ArticleListView.as_view(), name='all-articles'),
    path('<int:pk>/', include([
        path('<str:title>/', ArticleView.as_view(), name='single-article'),
        path('delete/', ArticleDeleteView.as_view(), name='article-create'),
    ])),
    path('user_articles/', ArticlesByUser.as_view(), name='user-articles'),
    path('create/', ArticleAddView.as_view(), name='article-create'),
]
