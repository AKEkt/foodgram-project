from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import TokenCreateSerializer
from djoser.serializers import UserSerializer
from djoser.conf import settings

User = get_user_model()


class MyTokenCreateSerializer(TokenCreateSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields[User.USERNAME_FIELD] = serializers.CharField(
            required=False
        )


class MyDjoserUserSerializer(UserSerializer):

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
        ) + ('is_subscribed',)
        read_only_fields = (settings.LOGIN_FIELD,)

    def get_is_subscribed(self, obj):
        return 'false'
