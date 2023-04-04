from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import TokenCreateSerializer
from djoser.serializers import UserSerializer
from .models import Follow
from djoser.conf import settings

User = get_user_model()


class MyTokenCreateSerializer(TokenCreateSerializer):
    settings.LOGIN_FIELD = User.USERNAME_FIELD


class MyDjoserUserSerializer(UserSerializer):

    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('is_subscribed',)

    def get_is_subscribed(self, obj):

        return Follow.objects.filter(
            user=self.context.get('request').user.id, author=obj.id
            ).exists()


class ListSubscripSerializer(MyDjoserUserSerializer):
    pass


class SubscripUserSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',
                  'recipes',
                  'recipes_count',)
        extra_kwargs = {'author': {'read_only': True},
                        'user': {'read_only': True}}

    def get_is_subscribed(self, obj):
        return True

    def get_recipes(self, obj):
        return 0

    def get_recipes_count(self, obj):
        return 0
