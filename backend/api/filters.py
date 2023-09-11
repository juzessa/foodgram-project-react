import django_filters as filters

from recipes.models import Recipe, User


class RecipeFilter(filters.FilterSet):
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all())
    cart = filters.BooleanFilter(
        widget=filters.widgets.BooleanWidget())
    favourite = filters.BooleanFilter(
        widget=filters.widgets.BooleanWidget())
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'favourite', 'cart']
