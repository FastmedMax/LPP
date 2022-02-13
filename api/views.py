from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import ListAPIView

from .models import User, Task, Award, Goods
from .serializers import UserSerializer, AwardSerializer, TaskSerializer, GoodsSerializer, UserCreateSerializer

# Create your views here.
class UserView(APIView):
    queryset = User
    serializer_class = UserSerializer

    def get(self, request, user_id):
        try:
            user = self.queryset.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response("Пользователь не найден!", status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            awards = Award.objects.all()
            serializer.instance.awards.add(*awards)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AwardListView(ListAPIView):
    queryset = Award
    serializer_class = AwardSerializer

    def get(self, request, *args, **kwargs):
        try:
            awards = self.queryset.objects.all()
        except Award.DoesNotExist:
            return Response("Награды не найдены!", status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(awards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskListView(ListAPIView):
    queryset = Task
    serializer_class = TaskSerializer

    def get(self, request, user_id, *args, **kwargs):
        try:
            if kwargs.get("day"):
                tasks = self.queryset.objects.filter(user_id=user_id, expired_at=kwargs["day"])
            else:
                tasks = self.queryset.objects.filter(user_id=user_id)
        except Task.DoesNotExist:
            return Response("Задачи не найдены!", status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskListWeekView(ListAPIView):
    queryset = Task
    serializer_class = TaskSerializer

    def get(self, request, user_id, *args, **kwargs):
        try:
            current_week = timezone.now().isocalendar()[1]
            tasks = self.queryset.objects.filter(user_id=user_id, expired_at__week=current_week)
        except Task.DoesNotExist:
            return Response("Задачи не найдены!", status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskView(APIView):
    queryset = Task
    serializer_class = TaskSerializer
    
    def get(self, request, task_id):
        try:
            task = self.queryset.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response("Задача не найдена!", status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        try:
            task = self.queryset.objects.get(id=request.data["task_id"])
        except Task.DoesNotExist:
            return Response("Задача не найдена!",status=status.HTTP_404_NOT_FOUND)
        if request.data.get("is_complete"):
            task.is_complete()
        serializer = self.serializer_class(task, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=False):
            serializer.update(task, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


