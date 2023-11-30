import datetime as dt

from django.shortcuts import get_object_or_404

from rest_framework import serializers, validators

from reviews.models import Comment, Category, Genre, Review, Title, TitleGenre
from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')
        validators = [
            validators.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email'),
                message='Имя пользователя и email должны отличаться!'
            )
        ]

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" запрещено!'
            )
        if User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует!'
            )
        if User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует!'
            )
        return data


class UserReceiveTokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        required=True
    )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" запрещено!'
            )
        return username


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

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug')
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug', many=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category', )
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
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = ('id', 'author', 'title', 'score', 'text', 'pub_date')
        model = Review
        read_only_fields = ('title',)

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
