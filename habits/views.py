from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from habits.models import Habits, Award
from habits.paginators import HabitsPagination
from habits.permissions import IsOwner
from habits.serializers import HabitsSerializer, AwardSerializer


class HabitsViewSet(viewsets.ModelViewSet):
    """ Класс представления вида ViewSet для модели Привычки """

    serializer_class = HabitsSerializer
    queryset = Habits.objects.all()
    pagination_class = HabitsPagination
    permission_classes = [IsOwner]

    def get_permissions(self):
        """ Разрешаем безопасные методы для публичных привычек """
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            habit = self.get_object()
            if habit.is_public:
                return [IsAuthenticatedOrReadOnly()]
        return super().get_permissions()


class AwardViewSet(viewsets.ModelViewSet):
    """ Класс представления вида ViewSet для модели Вознаграждение """

    serializer_class = AwardSerializer
    queryset = Award.objects.all()
    permission_classes = [IsOwner]
