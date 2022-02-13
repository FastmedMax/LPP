from django.urls import path

from .views import UserView, TaskListView, TaskListWeekView, GoodsView, TaskView


urlpatterns = [
    path("users/", UserView.as_view()),
    path("users/<str:user_id>/", UserView.as_view()),
    path("tasks/", TaskView.as_view()),
    path("tasks/<str:user_id>/", TaskListView.as_view()),
    path("tasks/week/<str:user_id>/", TaskListWeekView.as_view()),
    path("tasks/<str:user_id>/<str:day>/", TaskListView.as_view()),
    path("goods/buy/", GoodsView.as_view())
]
