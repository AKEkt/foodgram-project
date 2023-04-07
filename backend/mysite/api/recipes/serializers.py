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
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ('id',
                  'name',
                  'measurement_unit',
                  'amount',)

    def get_amount(self, obj):
        pass


class RecipesSerializer(serializers.ModelSerializer):
    ingredients = IngredientsSerializer(many=True)

    class Meta:
        model = Recipes
        fields = ('id',
                  'ingredients',
                  'name',)
