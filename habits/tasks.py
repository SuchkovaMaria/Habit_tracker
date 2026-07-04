from datetime import timezone

from celery import shared_task

from habits.models import Habit
from habits.services import send_tg_massege
from users.models import User


@shared_task
def mail_about_habits_execution():
    today = timezone.now()
    today_date = today.date()
    current_week_day = today.strftime('%w')
    django_week_day = int(current_week_day) + 1 if current_week_day != '0' else 1
    daily_habits = Habit.objects.filter(
        frequency_of_execution=Habit.DAILY,
        lead_time__hour=today.hour,
        lead_time__minute=today.minute,
        owner__is_active=True  # Проверка активности юзера через связь owner
    )
    weekly_habits = Habit.objects.filter(
        frequency_of_execution=Habit.WEEKLY,
        lead_time__hour=today.hour,
        lead_time__minute=today.minute,
        owner__is_active=True,
        lead_time__week_day=django_week_day
    )

    habits_execution = daily_habits | weekly_habits
    for habit in habits_execution:
        if habit.owner and habit.owner.tg_chat_id:
            massage = f"Пора браться за привычку{habit.name}. Все получится!"
            send_tg_massege(habit.owner.tg_chat_id, massage)
