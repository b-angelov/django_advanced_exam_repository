from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND

from izpitnik.articles.api.permissions import IsAuthorPermission, IsAuthorOnAllMethodsPermission
from izpitnik.articles.api.serializers import ArticleSerializer, LikesSerializer
from izpitnik.articles.models import Article, Likes
from izpitnik.orth_calendar.models import HolidayOccurrences


class AuthClass:
    permission_classes = [IsAuthenticatedOrReadOnly]

class ArtilceAPIView(AuthClass, ListAPIView):
    serializer_class = ArticleSerializer

    def get_object(self):
        obj = Article.objects.filter(author__is_active=True).order_by('pk')
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
        if self.request.GET.get('favorites') and self.request.user.is_authenticated:
            obj = obj.filter(likes__user=self.request.user)
        return obj

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            "request": self.request
        })
        return context

    def get_queryset(self):

        queryset = self.get_object().all()
        return queryset


class CreateArticleAPIView(CreateAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthorPermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class GetUpdateDeleteArticleAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOnAllMethodsPermission]
    serializer_class = ArticleSerializer
    lookup_url_kwarg = "id"

    def get_queryset(self):
        queryset = Article.objects.filter(id=self.kwargs['id'])#,author=self.request.user.pk)
        return queryset

    def perform_update(self, serializer):
        serializer.save()#(author=self.request.user)

class ArticleLikeApiView(AuthClass, CreateAPIView):
    serializer_class = LikesSerializer

    def post(self, request, *args, **kwargs):
        article_id = self.kwargs.get('id')
        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            raise NotFound(detail="Article not found", code=HTTP_404_NOT_FOUND)
        likes = Likes.objects.filter(article=article, user=self.request.user).first()
        liked = False
        if likes:
            likes.delete()
        else:
            likes = Likes()
            likes.article = article
            likes.user = self.request.user
            likes.save()
            liked = True
        article.save()
        serializer = self.get_serializer({}, context={"article":article,"user":self.request.user})
        return Response(serializer.data, status=status.HTTP_200_OK)

