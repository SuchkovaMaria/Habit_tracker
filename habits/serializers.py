from recurrence.fields import RecurrenceField
from rest_framework import serializers

from habits.models import Habit
from habits.validators import validete_frequency_reward, validete_time_to_execute


class HabitSerializer(serializers.ModelSerializer):

    time_to_execute = serializers.DurationField(validators=[validete_time_to_execute])
    frequency_of_execution = RecurrenceField(validators=[validete_time_to_execute])
    connected_habit = serializers.PrimaryKeyRelatedField(
        queryset=Habit.objects.filter(nice_habit=True), allow_null=True, required=False, label="Связанная привычка"
    )

    class Meta:
        model = Habit
        fields = [
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
        ]
        read_only_fields = ("owner",)

        validators = [validete_frequency_reward]
