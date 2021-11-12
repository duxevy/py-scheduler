# Django imports
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Datetime imports
from datetime import timedelta


# Подсчет следующего дня
def next_day():
    return timezone.now() + timedelta(days=1)


# Основная модель
class Note(models.Model):
    STATUS = (
        (0, 'Не выполнено'),
        (1, 'Выполнено'),
        (2, 'Отложено')
    )
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    message = models.TextField(default='', verbose_name='Текст')
    date_add = models.DateTimeField(default=next_day, verbose_name='Время изменения')
    public = models.BooleanField(default=False, verbose_name='Опубликовать')
    important = models.BooleanField(default=False, verbose_name='Важность')
    author = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=False)

    def __str__(self):
        """Возвращает строковое представление модели"""
        return self.title
