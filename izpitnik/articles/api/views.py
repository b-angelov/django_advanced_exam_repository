from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND

from izpitnik.articles.api.permissions import IsAuthorPermission
from izpitnik.articles.api.serializers import ArticleSerializer
from izpitnik.articles.models import Article
from izpitnik.orth_calendar.models import HolidayOccurrences


class AuthClass:
    permission_classes = [IsAuthenticatedOrReadOnly]

class ArtilceAPIView(AuthClass, ListAPIView):
    serializer_class = ArticleSerializer

    def get_object(self):
        obj = Article.objects.all()
        if self.request.GET.get('id'):
            try:
                obj.get(pk=self.request.GET.get('id'))
                obj = obj.filter(pk=self.request.GET.get('id'))
            except Article.DoesNotExist:
                raise NotFound(detail="Article not found", code=HTTP_404_NOT_FOUND)
        if self.request.GET.get('date'):
            try:
                objh = HolidayOccurrences(date=self.request.GET.get('date')).object_by_date()
                obj = obj.filter(Q(saint__in=objh.saint) | Q(feast__in=objh.feast))
            except ValueError:
                raise ParseError(detail="Incorrect date value", code=400)
        if self.request.GET.get('feast'):
            obj = obj.filter(feast=self.request.GET.get('feast'))
        if self.request.GET.get('saint'):
            obj = obj.filter(saint=self.request.GET.get('saint'))
        if self.request.GET.get('holiday'):
            obj = obj.filter(holiday=self.request.GET.get('holiday'))
        if self.request.GET.get('author'):
            obj = obj.filter(author=self.request.GET.get('author'))
        return obj

    def get_queryset(self):

        queryset = self.get_object().all()
        return queryset


class CreateArticleAPIView(CreateAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthorPermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
