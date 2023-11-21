from django.shortcuts import get_object_or_404

from rest_framework import viewsets, filters, mixins

from reviews.models import Title, Genre, Category, Review, Title
from api.serializers import (TitleChangeSerializer,
                             TitleReadSerializer,
                             GenreSerializer,
                             CategorySerializer,
                             CommentSerializer,
                             ReviewSerializer)
from api.permissions import IsAuthorModerAdminOrReadOnly


class TitleViewSet(viewsets.ModelViewSet):
    '''Viewset для модели Title'''
    queryset = Title.objects.all()
    permission_classes = ()
    filter_backends = filters.SearchFilter
    filterset_fields = ('name', 'year', 'category', 'genre',)
    http_method_names = ['get', 'post', 'patch', 'delete',]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleReadSerializer
        else:
            return TitleChangeSerializer


class GenreCategoryViewSet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet,):
    permission_classes = ()
    filter_backends = filters.SearchFilter
    filterset_fields = ('name',)


class GenreViewSet(GenreCategoryViewSet):
    '''Vieset для модели Genre'''
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(GenreCategoryViewSet):
    '''Viewset для модели Category'''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModerAdminOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModerAdminOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())
