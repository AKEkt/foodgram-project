from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (DownloadShopCart, FavoriteViewSet, RecipesViewSet,
                    ShoppingCartViewSet)

router = DefaultRouter()
router.register(r'', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('download_shopping_cart/', DownloadShopCart.as_view()),
    path('<int:pk>/favorite/', FavoriteViewSet.as_view()),
    path('<int:pk>/shopping_cart/', ShoppingCartViewSet.as_view()),
    path('', include(router.urls)),
]
