from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from habits.models import Habits, Award
from habits.paginators import HabitsPagination
from habits.permissions import IsOwner
from habits.serializers import HabitsSerializer, AwardSerializer
from habits.tasks import reminder_of_habit


class HabitsViewSet(viewsets.ModelViewSet):
    """ Класс представления вида ViewSet для модели Привычки """

    serializer_class = HabitsSerializer
    queryset = Habits.objects.all().order_by('id')
    pagination_class = HabitsPagination
    permission_classes = [IsOwner]

    def get_permissions(self):
        """ Разрешаем безопасные методы для публичных привычек """

        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            if self.action == 'list':
                return super().get_permissions()

            if self.action == 'retrieve':
                habit = self.get_object()
                if habit.is_public:
                    return [IsAuthenticatedOrReadOnly()]
        return super().get_permissions()

    def perform_create(self, serializer):
        """ Метод вносит изменение в сериализатор создания "Привычки" """

        habit = serializer.save(user=self.request.user)
        tg_chat_id = self.request.user.tg_chat_id
        # Запускаем периодическую задачу
        reminder_of_habit(habit.id, tg_chat_id, habit.name, habit.periodicity)

    def get_queryset(self):
        """ Метод для изменения запроса к базе данных по объектам модели "Курса". """

        return Habits.objects.filter(user=self.request.user)


class AwardViewSet(viewsets.ModelViewSet):
    """ Класс представления вида ViewSet для модели Вознаграждение """

    serializer_class = AwardSerializer
    queryset = Award.objects.all()
    permission_classes = [IsOwner]
