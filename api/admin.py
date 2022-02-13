from django.contrib import admin

from .models import User, Task, Award, Goods

# Register your models here.
admin.site.register(Award)
admin.site.register(Goods)


class UserAwardlist(admin.StackedInline):
    model = User.awards.through
    extra = 0
    classes = ["collapse"]


class UserGoodsList(admin.StackedInline):
    model = User.goods.through
    extra = 0
    classes = ["collapse"]


class UserTasksList(admin.StackedInline):
    model = Task
    extra = 0
    classes = ["collapse"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (UserAwardlist, UserGoodsList, UserTasksList)
    exclude = ("goods",)