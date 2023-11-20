from rest_framework import viewsets, filters

from reviews.models import Title, Genre, Category
from api.serializers import (TitleSerializer,
                             GenreSerializer,
                             CategorySerializer)


class TitleViewSet(viewsets.ModelViewSet):
    '''Viewset для модели Title'''
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = ()
    filter_backends = filters.SearchFilter
    filterset_fields = ('name', 'year', 'category', 'genre',)
    http_method_names = ['get', 'post', 'patch', 'delete',]


class GenreViewSet(viewsets.ModelViewSet):
    '''Vieset для модели Genre'''
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = ()
    filter_backends = filters.SearchFilter
    filterset_fields = ('name',)


class CategoryViewSet(viewsets.ModelViewSet):
    '''Viewset для модели Category'''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = ()
    filter_backends = filters.SearchFilter
    filterset_fields = ('name',)
