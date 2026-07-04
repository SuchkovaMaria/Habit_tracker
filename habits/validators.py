from datetime import timedelta
from django.utils import timezone
from rest_framework.serializers import ValidationError


def validete_time_to_execute(value):
    """Проверка времени выполнения"""

    if value > timedelta(seconds=120):
        raise ValidationError("Недопускается более 120 секунд")
    elif value <= timedelta(seconds=0):
        raise ValidationError("Недопускается отрицательное время")


# def validete_frequency_of_execution(value):
#     """Проверка периодичности"""
#
#     frequency = ["Ежедневно", "Раз в неделю"]
#     if value not in frequency:
#         raise ValidationError("Недопускается более 120 секунд")


def validete_frequency_reward(attrs):
    """Проверка старта привычки и взаимоисключения вознаграждения и связанной привычки"""

    # 1. Проверка заполнености вознаграждения и связной привычки
    if attrs.get("connected_habit") and attrs.get("reward"):
        raise ValidationError("Недопускается указывать и связную привычку и вознаграздение. Выберите что то одно.")

    lead_time = attrs.get('lead_time')

    # 2. Проверка даты первого выполнения
    if lead_time:
        now = timezone.now()
        if lead_time < now:
            raise ValidationError("Дата и время выполнения не могут быть в прошлом.")

    # 3. Проверка даты первого выполнения на случай когда она отложена дальше, чем на 7 дней от текущего момента
        if lead_time > now + timedelta(days=7):
            raise ValidationError("Первое выполнение должно быть запланировано не позже, чем через 7 дней.")

    return attrs
