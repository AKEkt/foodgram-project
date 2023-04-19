import django_filters

from ..recipes.models import Recipes


class TagsFilterSet(django_filters.FilterSet):
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )

    class Meta:
        model = Recipes
        fields = ('tags',)
