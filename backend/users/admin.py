from django.contrib import admin
from django.contrib.auth import get_user_model
from recipes.models import (Favorite, Ingredient, RecipeIngred, Recipes,
                            ShoppingCart, Tag, TagRecipe)
from users.models import Follow

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name',)
    list_filter = ('email', 'last_name')
    empty_value_display = '-пусто-'


class RecipesAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'count')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'

    def count(self, inst):
        return Favorite.objects.filter(recipe=Recipes.objects.get
                                       (id=inst.id)).count()

    count.short_description = 'Число добавлений'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    list_filter = ('user', 'author',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class RecipeIngredAdmin(admin.ModelAdmin):
    list_display = ('recipesid', 'ingredient', 'amount',)
    list_filter = ('recipesid', 'ingredient', )
    list_editable = ('ingredient', 'amount',)
    empty_value_display = '-пусто-'


class TagRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipesid', 'tag',)
    list_filter = ('tag',)
    list_editable = ('tag',)
    empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_filter = ('recipe',)
    list_editable = ('recipe',)
    empty_value_display = '-пусто-'


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_filter = ('recipe',)
    list_editable = ('recipe',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Recipes, RecipesAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(RecipeIngred, RecipeIngredAdmin)
admin.site.register(TagRecipe, TagRecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
