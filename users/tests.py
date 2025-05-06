from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User


class TestUser(APITestCase):
    """ Тесты для модели пользователя  """

    # def setUp(self):
    #     self.user = User.objects.create_user(email="test1@gmail.com", password="123qaz123")

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email="test1@gmail.com", password="123qaz123")

    def test_user_post(self):
        """ Тестируем создание пользователя """
        url = reverse("users:user-list")
        data = {
            "email": "test@gmail.com",
            "password": "123qwe123"
        }
        response = self.client.post(url, data=data)
        data = response.json()
        self.assertEqual(data.get("email"), "test@gmail.com")

    def test_user_retrieve(self):
        """ Тестируем детализация пользователя """
        url = reverse("users:user-detail", args=(self.user.id,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(data.get("id"), 11)
        self.assertEqual(data.get("email"), "test1@gmail.com")

    def test_user_list(self):
        """ Тестируем просмотр списка пользователей """
        url = reverse("users:user-list")
        response = self.client.get(url)
        data = response.json()
        data_expect = [{'id': 11, 'name': None, 'email': 'test1@gmail.com', 'phone': None}]
        # print("data:", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, data_expect)

    def test_user_put(self):
        """ Тестируем обновление пользователя """

        url = reverse("users:user-detail", args=(self.user.id,))
        data = {
            "email": "test1@gmail.com",
            "password": "123qaz123",
            "phone": "79555555555"
        }
        response = self.client.put(url, data, content_type='application/json')
        data_json = response.json()
        # print(data_json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_json.get("phone"), data.get("phone"))

    def test_user_delete(self):
        """ Тестируем удаление пользователя """

        url = reverse("users:user-detail", args=(self.user.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
