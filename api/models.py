from django.db import models

# Create your models here.
class User(models.Model):
    id_vk = models.CharField(verbose_name="ID пользователя в VK", max_length="60")
    experience = models.IntegerField(verbose_name="Опыт пользователя")
    level = models.IntegerField(verbose_name="Уровень пользователя")
    coins = models.IntegerField(verbose_name="Количество монет у пользователя")
    picture_id = models.IntegerField(verbose_name="ID картинки")


class Task(models.Model):
    IMPORTANCE = [
        ("OPT", "Optional"),
        ("REQ", "Required"),
        ("URG", "Urgently"),
    ]

    FREQUENCY = [
        ("ONCE","Once"),
        ("DAY","Once_a_day"),
        ("WEEK","Once_a_week"),
    ]

    COMPLEXITY = [
        ("EASY","Easy"),
        ("MEDIUM","Medium"),
        ("HARD","Hard"),
    ]

    task_id = models.CharField(verbose_name="ID Задачи", max_length="60")
    name = models.CharField(verbose_name="Название задачи", max_length="60")
    picture = models.ImageField(verbose_name="Картинка задачи")
    description = models.TextField(verbose_name="Описание задачи")
    expired_at = models.DateField(verbose_name="Дата окончания задачи")
    importance = models.CharField(verbose_name="Важность задачи", max_length="60", choices=IMPORTANCE)
    frequency = models.CharField(verbose_name="Частота задачи", max_length="60", choices=FREQUENCY)
    complexity = models.CharField(verbose_name="Сложность", max_length="60", choices=COMPLEXITY)
    is_complete = models.BooleanField(verbose_name="Выполнена ли задача")
