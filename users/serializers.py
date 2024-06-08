from djoser.serializers import UserCreateSerializer


class UserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ("email", "password", "first_name", "last_name", "phone_number", "role")