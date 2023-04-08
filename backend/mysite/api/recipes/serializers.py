from rest_framework import serializers
from .models import Tag, Ingredient, Recipes, RecipIngred


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id',
                  'name',
                  'color',
                  'slug',)


class IngredientsSerializer(serializers.ModelSerializer):
    # amount = serializers.ReadOnlyField(source='amount')
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipIngred
        fields = ('id',
                  'name',
                  'measurement_unit',
                  'amount',)


class RecipesSerializer(serializers.ModelSerializer):
    ingredients = IngredientsSerializer(many=True, source='recip.all')

    class Meta:
        model = Recipes
        fields = ('id',
                  'ingredients',
                  'name',
                  'text',
                  'cooking_time')
