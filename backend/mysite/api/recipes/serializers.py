from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Ingredient, Recipes, Tag, RecipIngred, TagRecip
from ..serializers.serializers import MyDjoserUserSerializer, Base64ImageField

User = get_user_model()


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


class SubscripRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = ('id',
                  'name',
                  'image',
                  'cooking_time')


class IngredientRecipesSerializer(IngredientsSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta(IngredientsSerializer.Meta):
        model = RecipIngred
        fields = IngredientsSerializer.Meta.fields + ('amount',)


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = MyDjoserUserSerializer()
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
        return False

    def get_is_in_shopping_cart(self, obj):
        return False


class RecipesCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = IngredientRecipesSerializer(many=True)
    tags = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=3))

    class Meta:
        model = Recipes
        fields = ('tags',
                  'ingredients',
                  'name',
                  'image',
                  'text',
                  'cooking_time')

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
            TagRecip.objects.create(tag=curr_tags, recipesid=recip)
        return recip
