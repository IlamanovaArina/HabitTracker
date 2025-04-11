from datetime import timedelta

from rest_framework import serializers

from habits.models import Habits, Award


class HabitsSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Привычки """

    def validate_related_habit_or_award(self, related_habit, award):
        """ Проверяем, заполнены ли оба поля """
        if related_habit and award:
            raise serializers.ValidationError("Нельзя заполнять оба поля одновременно. "
                                              "Заполните либо related_habit, либо award.")

    def validate_time_to_complete(self, time_to_complete):
        """ Проверяет время выполнения """
        if time_to_complete > timedelta(seconds=120):
            raise serializers.ValidationError("Время выполнения не должно превышать 120 секунд.")

    def validate_related_habit_in_pleasant_habits_sign(self, related_habit_id):
        """ К привычке можно привязать только приятную привычку """
        related_habit = Habits.objects.filter(id=related_habit_id).first()
        if related_habit is None or not related_habit.pleasant_habits_sign:
            raise serializers.ValidationError("Вы можете привязать только приятную привычку.")

    def validate_pleasant_habits_sign(self, pleasant_habits_sign, related_habit, award):
        """ У приятной привычки не может быть вознаграждения или связанной привычки """
        if pleasant_habits_sign and (related_habit or award):
            raise serializers.ValidationError("У приятной привычки не может быть "
                                              "вознаграждения или связанной привычки")

    def validate_periodicity(self, periodicity):
        """ Нельзя выполнять привычку реже чем 1 раз в 7 дней """
        if periodicity < 1 or periodicity > 7:
            raise serializers.ValidationError("Периодичность должна быть в диапазоне от 1 до 7.")

    def validate(self, attrs):
        self.validate_related_habit_or_award(attrs.get('related_habit'), attrs.get('award'))
        self.validate_time_to_complete(attrs.get('time_to_complete'))
        self.validate_related_habit_in_pleasant_habits_sign(attrs.get('related_habit'))
        self.validate_pleasant_habits_sign(attrs.get('pleasant_habits_sign'), attrs.get('related_habit'), attrs.get('award'))
        self.validate_periodicity(attrs.get('periodicity'))
        return attrs

    class Meta:
        fields = '__all__'
        model = Habits


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Award
