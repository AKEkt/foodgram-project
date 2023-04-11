from api.recipes.models import (Favorite, Ingredient, Recipes, RecipIngred,
                                Tag, TagRecip, ShoppingCart)
from django.contrib import admin
from django.contrib.auth import get_user_model

# from import_export import resources
# from import_export.admin import ImportExportModelAdmin
from .models import Follow

User = get_user_model()
admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipes)
admin.site.register(RecipIngred)
admin.site.register(TagRecip)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
