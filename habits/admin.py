from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "place",
        "lead_time",
        "action",
        "nice_habit",
        "connected_habit",
        "time_to_execute",
        "frequency_of_execution",
        "reward",
        "public",
        "owner",
    )
    list_editable = ("name", "lead_time", "owner")
