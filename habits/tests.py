from datetime import datetime, timedelta
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from habits.tasks import mail_about_habits_execution
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="user_test@test.com", tg_chat_id="111111111")
        self.habit = Habit.objects.create(
            name="first_test_course",
            owner=self.user,
            place="test",
            lead_time=datetime.now() + timedelta(minutes=5),
            action="test_action",
            nice_habit=True,
            time_to_execute="19",
            frequency_of_execution="Ежедневно",
            reward="test_reward",
        )
        self.client.force_authenticate(user=self.user)

    def test_hibit_retrive(self):
        """Проверка доступа к привычке"""

        today = datetime.now()
        lead_time_test = today + timedelta(minutes=10)
        habit_test = Habit.objects.create(
            name="first_test_course",
            owner=self.user,
            place="test",
            lead_time=lead_time_test,
            action="test_action",
            nice_habit=True,
            time_to_execute="89",
            frequency_of_execution="Ежедневно",
            reward="test_reward",
        )
        url = reverse("habits:habit-detail", args=[habit_test.pk])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), habit_test.name)

    def test_hibit_create(self):
        """Проверка создания привычки"""

        today = datetime.now()
        lead_time_test = today + timedelta(minutes=10)
        url = reverse("habits:habit-create")
        data = {
            "name": "first_test_course",
            "place": "test",
            "lead_time": lead_time_test,
            "action": "test_action",
            "nice_habit": True,
            "time_to_execute": "89",
            "frequency_of_execution": "Ежедневно",
            "reward": "test_reward",
            "owner": 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_hibit_create_valid_1(self):
        """Проверка времени старта привычки при создании"""

        url = reverse("habits:habit-create")
        data = {
            "name": "first_test_course",
            "place": "test",
            "lead_time": "2026-07-04T13:14:00",
            "action": "test_action",
            "nice_habit": True,
            "time_to_execute": "89",
            "frequency_of_execution": "Ежедневно",
            "reward": "test_reward",
            "owner": 1,
        }
        response = self.client.post(url, data)
        print("\nОШИБКИ ВАЛИДАЦИИ:", response.data.get("non_field_errors"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.all().count(), 1)

    def test_hibit_create_valid_2(self):
        """Проверка времени выполнения привычки при создании"""

        today = datetime.now()
        lead_time_test = today + timedelta(minutes=10)
        url = reverse("habits:habit-create")
        data = {
            "name": "first_test_course",
            "place": "test",
            "lead_time": lead_time_test,
            "action": "test_action",
            "nice_habit": True,
            "time_to_execute": "130",
            "frequency_of_execution": "Ежедневно",
            "reward": "test_reward",
            "owner": 1,
        }
        response = self.client.post(url, data)
        print("\nОШИБКИ ВАЛИДАЦИИ:", response.data.get("time_to_execute"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.all().count(), 1)

    def test_hibit_create_valid_3(self):
        """Проверка запрета заполненость связной привычки и вознаграждения при создании"""

        today = datetime.now()
        lead_time_test = today + timedelta(minutes=10)
        url = reverse("habits:habit-create")

        data = {
            "name": "first_test_course",
            "place": "test",
            "lead_time": lead_time_test,
            "action": "test_action",
            "nice_habit": True,
            "connected_habit": self.habit.pk,
            "time_to_execute": "120",
            "frequency_of_execution": "Ежедневно",
            "reward": "test_reward",
            "owner": 1,
        }
        response = self.client.post(url, data)
        print("\nОШИБКИ ВАЛИДАЦИИ:", response.data.get("non_field_errors"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.all().count(), 1)

    def test_hibit_update(self):
        """Проверка изменения привычки"""
        url = reverse("habits:habit-update", args=[self.habit.pk])
        data = {"name": "test_habit_two_update"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "test_habit_two_update")

    def test_hibit_delete(self):
        """Проверка удаления привычки"""
        url = reverse("habits:habit-delete", args=[self.habit.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    @patch("habits.tasks.send_tg_massege")
    def test_task(self, mock_send_tg):
        """Проверка отправки сообщения в ТГ"""

        today = datetime.now()

        habit_test = Habit.objects.create(
            name="first_test_course",
            owner=self.user,
            place="test",
            lead_time=today,
            action="test_action",
            nice_habit=True,
            time_to_execute="89",
            frequency_of_execution="Ежедневно",
            reward="test_reward",
        )
        mail_about_habits_execution()

        # 4. Проверяем, что мок был успешно вызван
        self.assertTrue(mock_send_tg.called)

        # 5. Проверяем, с какими именно аргументами вызвалась функция
        expected_message = f"Пора браться за привычку {habit_test.name}. Все получится!"
        mock_send_tg.assert_called_once_with("111111111", expected_message)
