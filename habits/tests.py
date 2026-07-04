from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import Group

from habits.models import Habit
from users.models import User

# class HabitTestCase(APITestCase):
#
#     def setUp(self):
#         self.user = User.objects.create_user(email='user_test@test.com', )
#         self.habit = Habit.objects.create(name="first_test_course", owner=self.user)
#
#         self.client.force_authenticate(user=self.user)
#
#     def test_lesson_retrive(self):
#         url = reverse('course:lesson-detail', args=[self.lesson.pk])
#         response = self.client.get(url)
#         data = response.json()
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(data.get('name'), self.lesson.name)
#
#     def test_lesson_create(self):
#         url = reverse('course:lesson-create')
#         data = {"name": "test_leasson_two", "course": 1, "video_path": "https://youtube.com//test2", "owner": 1}
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Lesson.objects.all().count(), 2)
#
#     def test_lesson_create_valid(self):
#         url = reverse('course:lesson-create')
#         data = {"name": "test_leasson_two", "course": 1, "video_path": "https://youtube//test2", "owner": 1}
#         response = self.client.post(url, data)
#         print("\nОШИБКИ ВАЛИДАЦИИ:", response.data.get("video_path"))
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(Lesson.objects.all().count(), 1)
#
#     def test_lesson_update(self):
#         url = reverse('course:lesson-update', args=[self.lesson.pk])
#         data = {"name": "test_leasson_two_update"}
#         response = self.client.patch(url, data)
#         data = response.json()
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(data.get('name'), "test_leasson_two_update")
#
#     def test_lesson_delete(self):
#         url = reverse('course:lesson-delete', args=[self.lesson.pk])
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Lesson.objects.all().count(), 0)
