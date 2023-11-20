from rest_framework import serializers, validators
import datetime as dt

from reviews.models import Title, Genre, Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleReadSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category', )
        model = Title


class TitleChangeSerializer(serializers.ModelSerializer):

    genre = serializers.SlugRelatedField(slug_field='name',
                                         queryset=Genre.objects.all(),
                                         many=True)
    category = serializers.SlugRelatedField(slug_field='name',
                                            queryset=Category.objects.all())

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category', )
        model = Title
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Genre.objects.all(),
                fields=('title', 'genre'),
                message='Этот жанр уже добавлен')
        ]

    def validate_year(self, value):
        if value < dt.date.today().year:
            return value
        raise serializers.ValidationError('Гостей из будущего не ждали')
