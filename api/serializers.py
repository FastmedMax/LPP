from rest_framework import serializers
from .models import User, Award, Task, Goods, UserAward


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = "__all__"


class UserAwardSerializer(serializers.ModelSerializer):
    picture = serializers.CharField(source="award.picture")
    description = serializers.ReadOnlyField(source="award.description")
    name = serializers.ReadOnlyField(source="award.name")
    max_progress = serializers.ReadOnlyField(source="award.max_progress")

    class Meta:
        model = UserAward
        exclude = ("user", "award")


class UserSerializer(serializers.ModelSerializer):
    awards = UserAwardSerializer(many=True, source="useraward_set")

    class Meta:
        model = User
        fields = "__all__"


