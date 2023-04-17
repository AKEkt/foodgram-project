from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import generics, mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import TagsFilterSet
from .models import (Favorite, Ingredient, Recipes, RecipIngred, ShoppingCart,
                     Tag)
from .serializers import (IngredientsSerializer, RecipesCreateSerializer,
                          RecipesSerializer, SubscripRecipesSerializer,
                          TagSerializer)

User = get_user_model()


class TagsViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ['get']


class IngredientsViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pagination_class = None
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    http_method_names = ['get']

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        name = self.request.query_params.get("name", None)

        if name is not None:
            print(name)
            return queryset.filter(name__istartswith=name)
        return queryset


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TagsFilterSet

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipesSerializer
        return RecipesCreateSerializer

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        is_favorited = self.request.query_params.get('is_favorited', None)
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart', None
        )
        author = self.request.query_params.get('author', None)
        if author is not None:
            queryset = queryset.filter(author=author)
        if is_favorited:
            queryset = queryset.filter(favrecip__user=self.request.user)
        elif is_in_shopping_cart:
            return queryset.filter(shoprecip__user=self.request.user)
        return queryset


class FavoriteViewSet(generics.CreateAPIView, generics.DestroyAPIView):
    http_method_names = ['post', 'delete']

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
                    'выполнено': 'Рецепт успешно удален из избранного!'
                }, status=status.HTTP_204_NO_CONTENT)
        return Response(
            {
                'ошибка': 'Объект не найден!'
            }, status=status.HTTP_400_BAD_REQUEST)


class ShoppingCartViewSet(generics.CreateAPIView, generics.DestroyAPIView):
    http_method_names = ['post', 'delete']

    def create(self, request, *args, **kwargs):
        recip = get_object_or_404(Recipes, id=self.kwargs.get('pk'))
        if ShoppingCart.objects.filter(shoprecipe=recip,
                                       user=self.request.user).exists():
            return Response(
                {
                    'ошибка': 'Рецепт уже есть в списке покупок!'
                }, status=status.HTTP_400_BAD_REQUEST)
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
                    'выполнено': 'Рецепт успешно удален из списка покупок!'
                }, status=status.HTTP_204_NO_CONTENT)
        return Response(
            {
                'ошибка': 'Объект не найден!'
            }, status=status.HTTP_400_BAD_REQUEST)


class DownloadShopCart(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        recipes = Recipes.objects.filter(shoprecip__user=self.request.user)
        list_recip_ing = []
        for recip in recipes:

            recip_ing = RecipIngred.objects.filter(recipesid=recip)
            list_recip_ing += recip_ing
            ingred = []
        for item in list_recip_ing:
            name = Ingredient.objects.get(name=item.ingredient).name
            measurement_unit = Ingredient.objects.get(
                name=item.ingredient
            ).measurement_unit
            amount = item.amount
            if name in ingred:
                ingred[ingred.index(name) + 2] += amount
            else:
                ingred += (name, measurement_unit, amount)

        response = HttpResponse(content_type='application/pdf')
        response[
            'Content-Disposition'
        ] = 'attachment; filename="Ingredients.pdf"'
        c = canvas.Canvas(response)
        pdfmetrics.registerFont(TTFont('TimesNewRomanRegular',
                                       'TimesNewRomanRegular.ttf'))
        c.setFont("TimesNewRomanRegular", 18)
        c.drawString(100, 750, 'Cписок покупок:')
        c.setFont("TimesNewRomanRegular", 14)
        y = 700
        for indx in range(0, len(ingred), 3):
            string = (f' *  {ingred[indx]} '
                      f'({ingred[indx+1]})   —   {str(ingred[indx+2])}')
            c.drawString(100, y, string)
            y -= 20
        c.showPage()
        c.save()
        return response
