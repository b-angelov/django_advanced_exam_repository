from django.urls import path, include

from izpitnik.articles.views import ArticleListView, ArticlesOnDate, ArticleView

urlpatterns = [
    # path('', ArticleListView.as_view()),
    path('', ArticleListView.as_view(), name='all-articles'),
    path('<int:pk>/<str:title>/', ArticleView.as_view(), name='single-article'),
]
