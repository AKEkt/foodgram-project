from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import TokenCreateSerializer


User = get_user_model()


class MyTokenCreateSerializer(TokenCreateSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields[User.USERNAME_FIELD] = serializers.CharField(
            required=False
        )
