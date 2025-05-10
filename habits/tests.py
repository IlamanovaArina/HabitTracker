import datetime
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from habits.models import Award, Habits
from users.models import User


class TestAward(APITestCase):
    """ Тесты для модели Вознаграждение  """

    def setUp(self):
        self.user = User.objects.create_user(email="test1@gmail.com", password="123qaz123")
        self.user.is_active = True
        self.user.save()
        self.client.force_authenticate(user=self.user)  # Авторизация
        self.award = Award.objects.create(name="Вознаграждение", user=self.user)

    def test_award_post(self):
        """ Тестируем создание объекта вознаграждение """
        url = reverse("habits:award-list")
        data = {
            "name": "Тестовое вознаграждение",
            "user": self.user.id,
            "price": 100,
        }
        response = self.client.post(url, data=data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get("price"), 100)

    def test_award_list(self):
        """ Тестируем просмотр списка вознаграждений """
        url = reverse("habits:award-list")
        response = self.client.get(url)
        data = response.json()
        data_expect = {'count': 1, 'next': None, 'previous': None, 'results': [
            {'id': 1, 'name': 'Вознаграждение', 'description': None, 'price': None, 'user': 1}
        ]}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, data_expect)

    def test_award_retrieve(self):
        """ Тестируем детализация объекта вознаграждение """
        url = reverse("habits:award-detail", args=(self.award.id,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(data.get("id"), 1)
        self.assertEqual(data.get("name"), "Вознаграждение")

    def test_award_put(self):
        """ Тестируем обновление объекта вознаграждение """

        url = reverse("habits:award-detail", args=(self.award.id,))
        data = {
            "name": "Вознаграждение изменено",
            "price": 99,
        }
        response = self.client.put(url, data, content_type='application/json')
        data_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_json.get("prise"), data.get("prise"))

    def test_award_delete(self):
        """ Тестируем удаление объекта вознаграждение """

        url = reverse("habits:award-detail", args=(self.user.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # def tearDown(self):
    #     self.user.delete()


class TestHabits(APITestCase):
    """ Тесты для модели Привычка  """

    def setUp(self):
        self.user = User.objects.create_user(email="test1@gmail.com", password="123qaz123")
        self.user.is_active = True
        self.user.save()
        self.client.force_authenticate(user=self.user)  # Авторизация
        self.award = Award.objects.create(name="Вознаграждение", user=self.user)
        self.habits_pleasant = Habits.objects.create(
            name="Чайная встреча",
            user=self.user,
            place="ТЦ Красная площадь",
            time=datetime.time(hour=12, minute=0),
            action="Встретиться с подругой за чашечкой чая",
            pleasant_habits_sign=True,
            periodicity=5,
            time_to_complete=datetime.timedelta(minutes=1)  # вместо "00:01:00"
        )
        self.habit = Habits.objects.create(
            name="Пробежка",
            user=self.user,
            place="Парк",
            time=datetime.time(hour=12, minute=0),
            action="Бегать",
            related_habit=self.habits_pleasant,
            periodicity=5,
            time_to_complete=datetime.timedelta(seconds=119)  # вместо "00:01:59"
        )

    def test_habits_post(self):
        """ Тестируем создание объекта привычка """
        url = reverse("habits:habit-list")
        data = {
            "user": self.user,
            "place": "ТЦ Красная площадь",
            "time": "12:00:00",
            "action": "Встретиться с подругой за чашечкой чая",
            "periodicity": 1,
            "award": self.award.id,
            "time_to_complete": "00:01:00"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_habits_retrieve(self):
        """ Тестируем детализация объекта привычка """
        url = reverse("habits:habit-detail", args=(self.habit.id,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(data.get("id"), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habits_list(self):
        """ Тестируем просмотр списка привычек """
        url = reverse("habits:habit-list")
        response = self.client.get(url)
        data = response.json()
        data_expect = {'count': 2, 'next': None, 'previous': None, 'results': [
            {'id': 1, 'name': 'Чайная встреча', 'place': 'ТЦ Красная площадь', 'time': '12:00:00',
             'action': 'Встретиться с подругой за чашечкой чая', 'pleasant_habits_sign': True, 'periodicity': 5,
             'time_to_complete': '00:01:00', 'is_public': False, 'user': 1, 'related_habit': None, 'award': None},
            {'id': 2, 'name': 'Пробежка', 'place': 'Парк', 'time': '12:00:00', 'action': 'Бегать',
             'pleasant_habits_sign': False, 'periodicity': 5, 'time_to_complete': '00:01:59', 'is_public': False,
             'user': 7, 'related_habit': 3, 'award': None}]}

        # print("data", data)
        # print("data_expect", data_expect)

        # #
        # data = {'count': 2, 'next': None, 'previous': None, 'results': [
        #     {'id': 1, 'name': 'Чайная встреча', 'place': 'ТЦ Красная площадь', 'time': '12:00:00',
        #      'action': 'Встретиться с подругой за чашечкой чая', 'pleasant_habits_sign': True, 'periodicity': 5,
        #      'time_to_complete': '00:01:00', 'is_public': False, 'user': 1, 'related_habit': None, 'award': None},
        #     {'id': 2, 'name': 'Пробежка', 'place': 'Парк', 'time': '12:00:00', 'action': 'Бегать',
        #      'pleasant_habits_sign': False, 'periodicity': 5, 'time_to_complete': '00:01:59', 'is_public': False,
        #      'user': 1, 'related_habit': 1, 'award': None}]}
        # data_expect = {'count': 2, 'next': None, 'previous': None, 'results': [
        #     {'id': 1, 'name': 'Чайная встреча', 'place': 'ТЦ Красная площадь', 'time': '12:00:00',
        #      'action': 'Встретиться с подругой за чашечкой чая', 'pleasant_habits_sign': True, 'periodicity': 5,
        #      'time_to_complete': '00:01:00', 'is_public': False, 'user': 7, 'related_habit': None, 'award': None},
        #     {'id': 4, 'name': 'Пробежка', 'place': 'Парк', 'time': '12:00:00', 'action': 'Бегать',
        #      'pleasant_habits_sign': False, 'periodicity': 5, 'time_to_complete': '00:01:59', 'is_public': False,
        #      'user': 7, 'related_habit': 3, 'award': None}]}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, data_expect)

    def test_habits_put(self):
        """ Тестируем обновление объекта привычка """

        url = reverse("habits:habit-detail", args=(self.habit.id,))
        data = {
            "user": self.user.id,
            "place": "ТЙ Галерея",
            "time": "13:00:00",
            "action": "Прогулка",
            "time_to_complete": "00:00:59",
            "award": self.award.id
        }
        # ..{'non_field_errors': ['Должно быть указано хотя бы одно из полей: связанная привычка или вознаграждение']}
        response = self.client.put(url, data, content_type='application/json')
        data_json = response.json()
        # print(data_json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_json.get("time_to_complete"), data.get("time_to_complete"))

    def test_habits_delete(self):
        """ Тестируем удаление объекта привычка """

        url = reverse("habits:habit-detail", args=(self.habit.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        """ Очистка тестовой дб каждый раз """
        self.user.delete()

# coverage run --source='.' manage.py. test
# coverage report
