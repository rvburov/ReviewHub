from rest_framework import viewsets, filters, mixins

from reviews.models import Title, Genre, Category
from api.serializers import (TitleChangeSerializer,
                             TitleReadSerializer,
                             GenreSerializer,
                             CategorySerializer)


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
