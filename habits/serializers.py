from rest_framework import serializers

from habits.models import Habits, Award


class HabitsSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Привычки """
    # user = serializers.IntegerField(read_only=True)

    def validate_related_habit_or_award(self, related_habit, award):
        """ Проверяем, заполнены ли оба поля """
        if related_habit and award:
            raise serializers.ValidationError("Нельзя заполнять оба поля одновременно. "
                                              "Заполните либо related_habit, либо award.")
        return related_habit, award

    def validate_time_to_complete(self, time_to_complete):
        """ Проверяет время выполнения """
        if time_to_complete:
            if time_to_complete.seconds > 120:
                raise serializers.ValidationError("Время выполнения не должно превышать 120 секунд.")
        return time_to_complete

    def validate_related_habit_in_pleasant_habits_sign(self, related_habit_id):
        """ К привычке можно привязать только приятную привычку """
        if related_habit_id:
            related_habit = Habits.objects.filter(id=related_habit_id).first()
            if related_habit is None or not related_habit.pleasant_habits_sign:
                raise serializers.ValidationError("Вы можете привязать только приятную привычку.")
        return related_habit_id

    def validate_periodicity(self, periodicity):
        """ Нельзя выполнять привычку реже чем 1 раз в 7 дней """
        if periodicity:
            if periodicity < 1 or periodicity > 7:
                raise serializers.ValidationError("Периодичность должна быть в диапазоне от 1 до 7.")
        return periodicity

    def validate(self, attrs):
        """ Валидация """
        pleasant_habits_sign = attrs.get('pleasant_habits_sign')
        related_habit = attrs.get('related_habit')
        award = attrs.get('award')

        # Проверяем условие: если pleasant_habits_sign True,
        # то нельзя указать related_habit и award одновременно
        if pleasant_habits_sign and (related_habit or award):
            raise serializers.ValidationError("У приятной привычки не может быть "
                                              "вознаграждения или связанной привычки")
        # Проверяем что хотя бы одно из полей указано: related_habit или award
        if not (related_habit or award) and not pleasant_habits_sign:
            raise serializers.ValidationError(
                "Должно быть указано хотя бы одно из полей: связанная привычка или вознаграждение")

        self.validate_related_habit_or_award(attrs.get('related_habit'), attrs.get('award'))
        self.validate_time_to_complete(attrs.get('time_to_complete'))
        self.validate_related_habit_in_pleasant_habits_sign(attrs.get('related_habit'))
        self.validate_periodicity(attrs.get('periodicity'))

        return attrs

    # def create(self, validated_data):
    #     """ Метод вносит изменение в сериализатор создания "Привычки" """
    #     user = self.context['request'].user  # Получаем текущего пользователя из контекста
    #     habit = Habits.objects.create(user=user, **validated_data)  # Передаем user в создание объекта
    #     return habit

    class Meta:
        fields = "__all__"
        model = Habits
        read_only_fields = ['user']


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Award
