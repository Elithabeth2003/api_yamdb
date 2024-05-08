from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Comment(models.Model):
    text = models.TextField('Текст комментария',)
    author = models.ForeignKey('User', verbose_name='Автор комментария')
    pub_date = models.DateTimeField('Дата публикации комментария', auto_now_add=True)
    review = models.ForeignKey('Review', related_name='comments', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return f'Комментарий {self.author} на {self.review}.'
    

class Review(models.Model):
    text = models.TextField('Текст отзыва',)
    author = models.ForeignKey('User', verbose_name='Автор отзыва')
    score = models.IntegerChoices('Оценка', 
                                  validators=[MaxValueValidator(10), MinValueValidator(1)])
    pub_date = models.DateTimeField('Дата публикации отзыва', auto_now_add=True)
    title = models.ForeignKey('Title', related_name='reviews', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

    def __str__(self):
        return f'Отзыв {self.author} на {self.title__name}.'
