from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'phone', 'password')
        extra_kwargs = {
            'password': {'write_only': True}  # Поле пароля доступно только для записи
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data.pop('password'))  # Удалите пароль из validated_data, прежде чем сохранить его
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))  # Хешируйте пароль при обновлении
        return super().update(instance, validated_data)
