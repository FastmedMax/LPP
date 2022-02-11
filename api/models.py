from django.db import models

# Create your models here.
class User(models.Model):
    id_vk = models.CharField(verbose_name="ID пользователя в VK", max_length="60")
    experience = models.IntegerField(verbose_name="Опыт пользователя")
    level = models.IntegerField(verbose_name="Уровень пользователя")
    coins = models.IntegerField(verbose_name="Количество монет у пользователя")
    picture_id = models.IntegerField(verbose_name="ID картинки")
