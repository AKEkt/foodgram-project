from django.contrib import admin
# from import_export import resources
# from import_export.admin import ImportExportModelAdmin
from .models import Follow
from api.recipes.models import Tag, Ingredient, Recipes, RecipIngred
from django.contrib.auth import get_user_model

User = get_user_model()
admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipes)
admin.site.register(RecipIngred)
