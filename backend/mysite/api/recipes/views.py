from .serializers import TagSerializer, IngredientsSerializer
from rest_framework import mixins
from rest_framework import viewsets
from .models import Tag, Ingredients


class TagsViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pagination_class = None
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
