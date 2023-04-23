import io

from django.contrib.auth import get_user_model
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, RecipeIngred, Recipes,
                            ShoppingCart, Tag)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from .filters import TagsFilterSet
from .mixins import CreateDestroyMixin
from .serializers import (IngredientsSerializer, RecipesCreateUpdateSerializer,
                          RecipesSerializer, TagSerializer)

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
        return RecipesCreateUpdateSerializer

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
            queryset = queryset.filter(favrecipe__user=self.request.user)
        elif is_in_shopping_cart:
            return queryset.filter(shoprecipe__user=self.request.user)
        return queryset


class FavoriteViewSet(CreateDestroyMixin):
    model = Favorite
    queryset = Favorite.objects.all()


class ShoppingCartViewSet(CreateDestroyMixin):
    model = ShoppingCart
    queryset = ShoppingCart.objects.all()


class DownloadShopCart(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        recipes = Recipes.objects.filter(shoprecipe__user=self.request.user)
        list_recipe_ing = []
        for recipe in recipes:

            recipe_ing = RecipeIngred.objects.filter(recipesid=recipe)
            list_recipe_ing += recipe_ing
            ingred = []
        for item in list_recipe_ing:
            name = Ingredient.objects.get(name=item.ingredient).name
            measurement_unit = Ingredient.objects.get(
                name=item.ingredient
            ).measurement_unit
            amount = item.amount
            if name in ingred:
                ingred[ingred.index(name) + 2] += amount
            else:
                ingred += (name, measurement_unit, amount)

        buffer = io.BytesIO()

        c = canvas.Canvas(buffer)
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
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True,
                            filename='Ingredientы.pdf')
