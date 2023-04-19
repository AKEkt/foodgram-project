from django.contrib import admin
from django.contrib.auth import get_user_model
from recipes.models import (Favorite, Ingredient, Recipes, RecipIngred,
                            ShoppingCart, Tag, TagRecip)
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
        return Favorite.objects.filter(favoritrecip=Recipes.objects.get
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


class RecipIngredAdmin(admin.ModelAdmin):
    list_display = ('recipesid', 'ingredient', 'amount',)
    list_filter = ('recipesid', 'ingredient', )
    list_editable = ('ingredient', 'amount',)
    empty_value_display = '-пусто-'


class TagRecipAdmin(admin.ModelAdmin):
    list_display = ('recipesid', 'tag',)
    list_filter = ('tag',)
    list_editable = ('tag',)
    empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'favoritrecip',)
    list_filter = ('favoritrecip',)
    list_editable = ('favoritrecip',)
    empty_value_display = '-пусто-'


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'shoprecipe',)
    list_filter = ('shoprecipe',)
    list_editable = ('shoprecipe',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Recipes, RecipesAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(RecipIngred, RecipIngredAdmin)
admin.site.register(TagRecip, TagRecipAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
