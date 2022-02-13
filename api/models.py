import enum

from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Award(models.Model):
    class Types(models.Choices):
        ENTHUSIAST = "Enthusiast"
        PUNCTUALITY = "Punctuality"
        HUNTER = "Hunter"
        EASY_DOES_IT = "Easy_does_it"

    picture = models.ImageField(verbose_name="Картинка награды")
    description = models.TextField(verbose_name="Описание награды")
    name = models.CharField(verbose_name="Название награды", max_length=60)
    max_progress = models.PositiveIntegerField(verbose_name="Максимальный прогресс для выполнения условия")
    type = models.CharField(verbose_name="Тип награды", max_length=60, choices=Types.choices)


class Goods(models.Model):
    picture = models.ImageField(verbose_name="Картинка товара")
    description = models.TextField(verbose_name="Описание товара")
    name = models.CharField(verbose_name="Название товара", max_length=60)
    price = models.PositiveIntegerField(verbose_name="Цена товара")


class User(models.Model):
    user_id = models.CharField(verbose_name="ID пользователя в VK", max_length=60, unique=True)
    experience = models.PositiveIntegerField(verbose_name="Опыт пользователя", default=0)
    level = models.PositiveIntegerField(verbose_name="Уровень пользователя", default=0)
    coins = models.PositiveIntegerField(verbose_name="Количество монет у пользователя", default=0)
    picture_id = models.ForeignKey(Goods, verbose_name="ID картинки", blank=True, on_delete=models.CASCADE, related_name="user_picture", null=True)
    goods = models.ManyToManyField(Goods, verbose_name="Картинки пользователя", blank=True)
    awards = models.ManyToManyField(Award, verbose_name="Награды пользователя", blank=True, through="UserAward")



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

    task_id = models.CharField(verbose_name="ID Задачи", max_length=60)
    name = models.CharField(verbose_name="Название задачи", max_length=60)
    picture = models.ImageField(verbose_name="Картинка задачи")
    description = models.TextField(verbose_name="Описание задачи")
    expired_at = models.DateField(verbose_name="Дата окончания задачи")
    importance = models.CharField(verbose_name="Важность задачи", max_length=60, choices=IMPORTANCE)
    frequency = models.CharField(verbose_name="Частота задачи", max_length=60, choices=FREQUENCY)
    complexity = models.CharField(verbose_name="Сложность", max_length=60, choices=COMPLEXITY)
    is_complete = models.BooleanField(verbose_name="Выполнена ли задача")


class Goods(models.Model):
    picture = models.ImageField(verbose_name="Картинка товара")
    description = models.TextField(verbose_name="Описание товара")
    name = models.CharField(verbose_name="Название товара", max_length=60)
    price = models.IntegerField(verbose_name="Цена товара")