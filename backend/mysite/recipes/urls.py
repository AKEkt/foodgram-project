from django.urls import path

from .views import (DownloadShopCart, FavoriteViewSet, RecipesViewSet,
                    ShoppingCartViewSet)

# from rest_framework.routers import DefaultRouter


# router = DefaultRouter()

# router.register(r'', RecipesViewSet, basename='recipes')
urlpatterns = [
    # path('', include(router.urls)),
    path('', RecipesViewSet.as_view()),
    path('download_shopping_cart/', DownloadShopCart.as_view()),
    path('<int:pk>/favorite/', FavoriteViewSet.as_view()),
    path('<int:pk>/shopping_cart/', ShoppingCartViewSet.as_view()),
]
