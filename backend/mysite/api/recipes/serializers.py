from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Ingredient, Recipes, Tag, RecipIngred, TagRecip, Favorite
from ..serializers.serializers import MyDjoserUserSerializer, Base64ImageField
from django.shortcuts import get_object_or_404

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
        return False

    def get_is_in_shopping_cart(self, obj):
        return False


class IngredientRecipesCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = RecipIngred
        fields = ('id',
                  'amount',)


class RecipesCreateSerializer(RecipesSerializer):
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


class FavoriteUserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    image = serializers.ReadOnlyField()
    cooking_time = serializers.ReadOnlyField()

    class Meta:
        model = Favorite
        fields = ('id',
                  'name',
                  'image',
                  'cooking_time',)
