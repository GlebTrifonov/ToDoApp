from django.db import models
from django.contrib.auth.models import User

class Categories(models.Model):
    category_name = models.CharField(max_length=50, verbose_name='Категория')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.category_name
    class Meta:
        verbose_name_plural = 'Категории'
        constraints = [
            models.UniqueConstraint(
                fields=['user','category_name'],
                name='unique_user_category'
            )
        ]


class Tasks(models.Model):
    class Priority(models.TextChoices):
        LOW = 'L', 'НИЗКИЙ'
        MID = 'M', 'СРЕДНИЙ'
        HIGHT = 'H', 'ВЫСОКИЙ'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    category = models.ManyToManyField(Categories, verbose_name='Категория')
    is_active = models.BooleanField(default=True, verbose_name='Статус выполнения')
    priority = models.CharField(max_length=1, choices=Priority.choices, default=Priority.MID, verbose_name='Приоритет')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Subtasks(models.Model):
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    is_active = models.BooleanField(default=True, verbose_name='Статус')
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, related_name='subtasks')
    def __str__(self):
        return self.title
    