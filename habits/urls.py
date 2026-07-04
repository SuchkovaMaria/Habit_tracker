from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitCreate, HabitDelete, HabitDetail, HabitList, HabitUpdate

app_name = HabitsConfig.name

urlpatterns = [
    path("habit_list/", HabitList.as_view(), name="habit-list"),
    path("habit_detail/<int:pk>/", HabitDetail.as_view(), name="habit-detail"),
    path("create/", HabitCreate.as_view(), name="habit-create"),
    path("habit/<int:pk>/update/", HabitUpdate.as_view(), name="habit-update"),
    path("habit/<int:pk>/delete/", HabitDelete.as_view(), name="habit-delete"),
]
