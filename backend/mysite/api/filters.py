import django_filters
from recipes import models


class TagsFilterSet(django_filters.FilterSet):
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )

    class Meta:
        model = models.Recipes
        fields = ('tags',)
