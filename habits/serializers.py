from rest_framework import serializers

from habits.models import Habits, Award


class HabitsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Habits


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Award
