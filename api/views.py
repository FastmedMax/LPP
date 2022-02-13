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


