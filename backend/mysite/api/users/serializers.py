from django.contrib.auth import get_user_model
from djoser.conf import settings
from djoser.serializers import TokenCreateSerializer
from rest_framework import serializers

from ..recipes.models import Recipes
from ..recipes.serializers import SubscripRecipesSerializer
from .models import Follow

User = get_user_model()


class MyTokenCreateSerializer(TokenCreateSerializer):
    settings.LOGIN_FIELD = User.USERNAME_FIELD


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
        return Follow.objects.filter(
            user=self.context['request'].user.id, author=obj.author.id
            ).exists()

    def get_recipes(self, obj):
        queryset = Recipes.objects.filter(author=obj.author.id)
        serializer = SubscripRecipesSerializer(queryset, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return Recipes.objects.filter(author=obj.author.id).count()
