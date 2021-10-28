import django_filters
from django_filters import rest_framework

from .models import Recipe, Tag


class CustomFilter(rest_framework.FilterSet):
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )

    class Meta:
        model = Recipe
        fields = ['tags', 'author']


