import datetime as dt
from rest_framework.validators import UniqueValidator

from django.shortcuts import get_object_or_404

from rest_framework import serializers, validators

from reviews.models import Comment, Category, Genre, Review, Title, TitleGenre
from users.models import User


class UserCreateSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        required=True
    )
    email = serializers.EmailField(
        max_length=254,
        required=True
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                f'Использовать имя - {value} - запрещено!'
            )
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                f'Пользователь с таким username — {value} — уже существует!'
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                f'Пользователь с таким email - {value} - уже существует!'
            )
        return value


class UserReceiveTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
    )
    confirmation_code = serializers.CharField(
        max_length=254,
        required=True
    )

class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]',
        required=True,
        max_length=150,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
    )
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleReadSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category', )
        model = Title


class TitleChangeSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug')
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug', many=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category', )
        model = Title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'review', 'text', 'pub_date')
        model = Comment
        read_only_fields = ('review',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = ('id', 'author', 'title', 'score', 'text', 'pub_date')
        model = Review
        read_only_fields = ('title',)
    
    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError('Оценка по 10-бальной шкале!')
        return value
    
    def validate(self, data):
        title_id = self.context['view'].kwargs['title_id']
        request = self.context['request']
        author = request.user
        title = get_object_or_404(Title, id=title_id)
        if (
            title.reviews.filter(author=author).exists()
            and request.method != 'PATCH'
        ):
            raise serializers.ValidationError(
                'Можно оставлять только один отзыв!'
            )
        return data
