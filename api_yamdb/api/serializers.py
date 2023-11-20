from rest_framework import serializers

from reviews.models import Title, Genre, Category


class TitleSerializer(serializers.ModelSerializer):

    # TODO написать кастомное поля с валидацией года
    # TODO написать валидацию однократной связи с жанром и категорией
    # TODO написать связь с категорией и жаром по слагу

    class Meta:
        fields = ('id', 'name', 'year', 'genre', 'category', 'description')
        model = Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category
