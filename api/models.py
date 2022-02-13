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

    picture = models.ImageField(verbose_name="Картинка награды", blank=True)
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

    def clean(self) -> None:
        if not self.id:
            return
        if self.goods:
            goods_ids = self.goods.values_list("id", flat=True)
        if self.picture_id not in goods_ids:
            return ValidationError("This picture is not purchased")
        return super().clean()


class UserAward(models.Model):
    user = models.ForeignKey(User, verbose_name="ID пользователя", on_delete=models.CASCADE)
    award = models.ForeignKey(Award, verbose_name="ID награды", on_delete=models.CASCADE)
    progress = models.PositiveIntegerField(verbose_name="Прогресс награды", default=0)
    is_complete = models.BooleanField(verbose_name="Получена ли награда", default=False)


class Task(models.Model):
    class Importance(models.Choices):
        OPTIONAL = "Optional"
        REQUIRED = "Required"
        URGENTLY = "Urgently"

    class Frequency(models.Choices):
        ONCE = "Once"
        DAY = "Once_a_day"
        WEEK = "Once_a_week"

    class Complexyty(models.Choices):
        EASY = "Easy"
        MEDIUM = "Medium"
        HARD = "Hard"

    user = models.ForeignKey(User, verbose_name="ID пользователя", related_name="tasks", on_delete=models.CASCADE, to_field="user_id")
    name = models.CharField(verbose_name="Название задачи", max_length=60)
    picture = models.ImageField(verbose_name="Картинка задачи", blank=True)
    description = models.TextField(verbose_name="Описание задачи", blank=True)
    created_at = models.DateField(verbose_name="Дата назначения задачи", auto_now=True)
    expired_at = models.DateField(verbose_name="Дата окончания задачи")
    importance = models.CharField(verbose_name="Важность задачи", max_length=60, choices=Importance.choices)
    frequency = models.CharField(verbose_name="Частота задачи", max_length=60, choices=Frequency.choices)
    complexity = models.CharField(verbose_name="Сложность", max_length=60, choices=Complexyty.choices)
    is_complete = models.BooleanField(verbose_name="Выполнена ли задача")

    def is_complete(self):
        awards = self.user.awards.through.objects.filter(is_complete=False)
        award_types = []
        if self.expired_at >= timezone.now().date():
            award_types.append(Award.Types.PUNCTUALITY.value)
            if (self.expired_at - self.created_at).days > 15:
                award_types.append(Award.Types.EASY_DOES_IT.value)
        coins = 5
        exp = 10
        if self.importance == self.Importance.OPTIONAL.value:
            coins += 1
            exp += 1
        elif self.importance == self.Importance.REQUIRED.value:
            coins += 10
            exp += 10
        elif self.importance == self.Importance.URGENTLY.value:
            coins += 20
            exp += 20
        
        if self.frequency == self.Frequency.DAY.value:
            coins += 5
            exp += 5
        elif self.frequency == self.Frequency.WEEK.value:
            coins += 7
            exp += 7

        if self.complexity == self.Complexyty.EASY.value:
            award_types.append(Award.Types.HUNTER.value)
        elif self.complexity == self.Complexyty.MEDIUM.value:
            coins = coins * 1.5
            exp = exp * 1.5
        elif self.complexity == self.Complexyty.HARD.value:
            award_types.append(Award.Types.ENTHUSIAST.value)
            coins = coins * 2
            exp = exp * 2

        self.user.coins += coins
        self.user.experience += exp

        # Update user awards progress
        for award_type in award_types:
            try:
                award = awards.get(award__type=award_type)
                award.progress += 1
                award.save()
            except UserAward.DoesNotExist:
                pass


        class Levels(enum.Enum):
            ONE = (1, 100)
            TWO = (2, 1000)
            THREE = (3, 1200)
            FOUR = (4, 1500)
            FIVE = (5, 1800)

            def __init__(self, num, requirement):
                self.num = num
                self.requirement = requirement


        for level in Levels:
            if self.user.level >= 5:
                continue
            if self.user.level != 0 and self.user.level <= level.num:
                continue
            if self.user.experience >= level.requirement:
                self.user.experience = self.user.experience - level.requirement
                self.user.level += 1
                break
        else:
            exp_requirement = 500*(self.user.level + 1)*4
            if self.user.experience >= exp_requirement:
                self.user.experience = self.user.experience - exp_requirement
                self.user.level += 1

        self.user.save()
