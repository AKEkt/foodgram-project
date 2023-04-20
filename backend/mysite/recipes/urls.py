from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (DownloadShopCart, FavoriteViewSet,
		    RecipesViewSet, ShoppingCartViewSet, TagsViewSet)


router = DefaultRouter()
router.register(r'', RecipesViewSet, basename='recipes')
urlpatterns = [
    path('', include(router.urls)),
    path('download_shopping_cart/', DownloadShopCart.as_view()),
    path('<int:pk>/favorite/', FavoriteViewSet.as_view()),
    path('<int:pk>/shopping_cart/', ShoppingCartViewSet.as_view()),
]
