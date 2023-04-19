from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.conf import settings
from djoser.serializers import TokenCreateSerializer, UserSerializer
from rest_framework import serializers

from ..recipes.models import (Favorite, Ingredient, Recipes, RecipIngred,
                              ShoppingCart, Tag, TagRecip)
from ..users.models import Follow
from .fields import Base64ImageField

User = get_user_model()


class MyTokenCreateSerializer(TokenCreateSerializer):
    settings.LOGIN_FIELD = User.USERNAME_FIELD


class MyDjoserUserSerializer(UserSerializer):

    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('is_subscribed',)

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=self.context['request'].user.id, author=obj.id
        ).exists()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id',
                  'name',
                  'color',
                  'slug',)


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id',
                  'name',
                  'measurement_unit',)


class IngredientRecipesSerializer(IngredientsSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True
    )

    class Meta(IngredientsSerializer.Meta):
        model = RecipIngred
        fields = IngredientsSerializer.Meta.fields + ('amount',)


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = MyDjoserUserSerializer(read_only=True)
    ingredients = IngredientRecipesSerializer(many=True,
                                              source='recip_ing.all')

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipes
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name',
                  'image',
                  'text',
                  'cooking_time')

    def get_is_favorited(self, obj):
        return Favorite.objects.filter(
            user=self.context['request'].user.id, favoritrecip=obj.id
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        return ShoppingCart.objects.filter(
            user=self.context['request'].user.id, shoprecipe=obj.id
        ).exists()


class IngredientRecipesCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = RecipIngred
        fields = ('id',
                  'amount',)


class RecipesCreateUpdateSerializer(RecipesSerializer):
    tags = serializers.ListField()
    ingredients = IngredientRecipesCreateSerializer(many=True)

    def to_representation(self, instance):
        request = self.context['request']
        return RecipesSerializer(instance, context={'request': request}).data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recip = Recipes.objects.create(**validated_data,
                                       author=self.context['request'].user)
        for ingredient in ingredients:
            id, amount = ingredient.values()
            curr_ingredient = Ingredient.objects.get(id=id)
            RecipIngred.objects.create(ingredient=curr_ingredient,
                                       recipesid=recip,
                                       amount=amount)
        for tag in tags:
            curr_tags = Tag.objects.get(id=tag)
            TagRecip.objects.create(recipesid=recip, tag=curr_tags)
        return recip

    def update(self, instance, validated_data):
        instance.image = validated_data.get("image", instance.image)
        instance.name = validated_data.get("name", instance.name)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get("cooking_time",
                                                   instance.cooking_time)
        RecipIngred.objects.filter(recipesid=instance).delete()
        ingredients = validated_data.get("ingredients")
        for ingredient in ingredients:
            id, amount = ingredient.values()
            curr_ingredient = get_object_or_404(Ingredient, id=id)
            RecipIngred.objects.create(ingredient=curr_ingredient,
                                       recipesid=instance, amount=amount)
        TagRecip.objects.filter(recipesid=instance).delete()
        tags = validated_data.get("tags")
        for tag in tags:
            curr_tags = get_object_or_404(Tag, id=tag)
            TagRecip.objects.create(recipesid=instance, tag=curr_tags)
        instance.save()
        return instance


class SubscripRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = ('id',
                  'name',
                  'image',
                  'cooking_time')


class SubscripUserSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
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
