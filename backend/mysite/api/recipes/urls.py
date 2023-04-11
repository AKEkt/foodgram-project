from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavoriteViewSet, IngredientsViewSet, RecipesViewSet,
                    TagsViewSet, ShoppingCartViewSet)

router_v1 = DefaultRouter()

router_v1.register(r'tags', TagsViewSet, basename='tags')
router_v1.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router_v1.register(r'recipes', RecipesViewSet, basename='recipes')
urlpatterns = [

    path('recipes/<int:pk>/favorite/', FavoriteViewSet.as_view()),
    path('recipes/<int:pk>/shopping_cart/', ShoppingCartViewSet.as_view()),
    path('', include(router_v1.urls)),

]
# /recipes/download_shopping_cart/
