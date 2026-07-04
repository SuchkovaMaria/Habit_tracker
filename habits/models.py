from django.db import models

from recurrence.fields import RecurrenceField

from users.models import User


class Habit(models.Model):
    """Модель привычки"""

    #Определяем варианты периодичности
    DAILY = "Ежедневно"
    WEEKLY = "Раз в неделю"

    FREQUENCY_CHOICES = [
        (DAILY, "Ежедневно"),
        (WEEKLY, "Раз в неделю"),
    ]

    name = models.CharField(
        max_length=100, verbose_name="Цель привычки", help_text="Укажите кратко и привлекательно цель привычки"
    )
    owner = models.ForeignKey("users.User", on_delete=models.SET_NULL, verbose_name="Пользователь", blank=True, null=True)
    place = models.CharField(max_length=100, verbose_name="Место", help_text="Укажите место выполнения привычки")
    lead_time = models.DateTimeField(
        verbose_name="Дата и время выполнения", help_text="Укажите дату и время выполнения привычки"
    )
    action = models.CharField(max_length=100, verbose_name="Действие", help_text="Укажите действие")
    nice_habit = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
        null=True,
    )
    connected_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Связная привычка",
        help_text="Выбирите связную привычку",
    )
    time_to_execute = models.DurationField(verbose_name="Время выполнения", help_text="Укажите время выполнения")
    frequency_of_execution = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES,
        default=DAILY,
        verbose_name="Периодичность",
        help_text="Укажите периодичность выполнения привычки: Ежедневно/Раз в неделю"
    )
    reward = models.CharField(
        max_length=100, verbose_name="Вознаграждение", blank=True, null=True, help_text="Укажите вознаграждение"
    )
    public = models.BooleanField(
        default=False,
        verbose_name="Признак публичности",
        null=True,
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = [
            "name",
        ]

    def __str__(self):
        return self.name
