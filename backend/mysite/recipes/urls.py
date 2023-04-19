from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (DownloadShopCart, FavoriteViewSet, IngredientsViewSet,
                    RecipesViewSet, ShoppingCartViewSet, TagsViewSet)

router = DefaultRouter()

router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'', RecipesViewSet, basename='recipes')
urlpatterns = [
    path('download_shopping_cart/', DownloadShopCart.as_view()),
    path('<int:pk>/favorite/', FavoriteViewSet.as_view()),
    path('<int:pk>/shopping_cart/', ShoppingCartViewSet.as_view()),
    path('', include(router.urls)),

]
