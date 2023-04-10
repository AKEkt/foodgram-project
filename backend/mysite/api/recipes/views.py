from rest_framework import mixins, viewsets

from .models import Ingredient, Recipes, Tag, Favorite
from .serializers import (IngredientsSerializer, RecipesSerializer,
                          TagSerializer, RecipesCreateSerializer, FavoriteUserSerializer)


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

class FavoriteViewSet(generics.CreateAPIView, generics.DestroyAPIView):
    serializer_class = FavoriteUserSerializer
    queryset = Favorite.objects.all()
    http_method_names = ['post', 'delete']

    def perform_create(self, serializer):
        author = get_object_or_404(User,
                                   id=self.kwargs.get('pk'))
        serializer.save(user=self.request.user, author=author)

    def delete(self, request, *args, **kwargs):
        author = get_object_or_404(User, id=self.kwargs.get('pk'))
        follow_user = Follow.objects.filter(user=self.request.user,
                                            author=author)
        if follow_user.exists():
            follow_user.delete()
            return Response(
                {
                    'выполнено': 'Успешная отписка'
                }, status=status.HTTP_204_NO_CONTENT)
        return Response(
            {
                'ошибка': 'Объект не найден'
            }, status=status.HTTP_400_BAD_REQUEST)