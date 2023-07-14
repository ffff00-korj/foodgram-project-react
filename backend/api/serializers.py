from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer создания нового пользователя."""

    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )
        lookup_field = 'username'

    def validate_username(self, username: str) -> str:
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Этот имя уже занято')
        return username
