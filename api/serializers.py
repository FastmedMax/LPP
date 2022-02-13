from rest_framework import serializers
from .models import User, Award, Task, Goods, UserAward


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = "__all__"


