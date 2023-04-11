from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status, viewsets
from rest_framework.response import Response

from .models import Favorite, Ingredient, Recipes, ShoppingCart, Tag
from .serializers import (IngredientsSerializer, RecipesCreateSerializer,
                          RecipesSerializer, SubscripRecipesSerializer,
                          TagSerializer)

User = get_user_model()


class TagsViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pagination_class = None
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipesSerializer
        return RecipesCreateSerializer

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        name = self.request.query_params.get("name", None)

        if name is not None:
            print(name)
            queryset = queryset.filter(name=name)

        return queryset


class FavoriteViewSet(generics.CreateAPIView, generics.DestroyAPIView):

    def create(self, request, *args, **kwargs):
        recip = get_object_or_404(Recipes, id=self.kwargs.get('pk'))
        Favorite.objects.create(favoritrecip=recip, user=self.request.user)
        serializer = SubscripRecipesSerializer(recip)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        recip = get_object_or_404(Recipes, id=self.kwargs.get('pk'))
        favorite = Favorite.objects.filter(favoritrecip=recip,
                                           user=self.request.user)
        if favorite.exists():
            favorite.delete()
            return Response(
                {
                    'выполнено': 'Рецепт успешно удален из избранного'
                }, status=status.HTTP_204_NO_CONTENT)
        return Response(
            {
                'ошибка': 'Объект не найден'
            }, status=status.HTTP_400_BAD_REQUEST)


class ShoppingCartViewSet(generics.CreateAPIView, generics.DestroyAPIView):

    def create(self, request, *args, **kwargs):
        recip = get_object_or_404(Recipes, id=self.kwargs.get('pk'))
        ShoppingCart.objects.create(shoprecipe=recip, user=self.request.user)
        serializer = SubscripRecipesSerializer(recip)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        recip = get_object_or_404(Recipes, id=self.kwargs.get('pk'))
        favorite = ShoppingCart.objects.filter(shoprecipe=recip,
                                               user=self.request.user)
        if favorite.exists():
            favorite.delete()
            return Response(
                {
                    'выполнено': 'Рецепт успешно удален из списка покупок'
                }, status=status.HTTP_204_NO_CONTENT)
        return Response(
            {
                'ошибка': 'Объект не найден'
            }, status=status.HTTP_400_BAD_REQUEST)


class DownloadShopCart(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        list_recip = ShoppingCart.objects.filter(user=self.request.user)
    pass
