from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.CharField(max_length=200)
    score = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
    )
    text = models.TextField("Текст", help_text="Отзыв")
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ["-pub_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_review"
            )
        ]
        verbose_name = 'Отзыв',
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return '"{}" - отзыв на "{}" Автор: "{}"'.format(
            self.text,
            self.title,
            self.author
        )


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField("Текст", help_text="Комментарий")
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = 'Комментарий',
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return '{} - комментарий на данный отзыв: {} Автор: {}'.format(
            self.text,
            self.review,
            self.author
        )
