import django_filters as filters
from recipes.models import Favourite, Recipe


class FavouriteFilter(filters.FilterSet):
    favourite = filters.BooleanFilter(
        widget=filters.widgets.BooleanWidget())

    class Meta:
        model = Favourite
        fields = ['recipe', 'favourite']


class RecipeFilter(filters.FilterSet):
    cart = filters.BooleanFilter(
        widget=filters.widgets.BooleanWidget())
    favourite = filters.BooleanFilter(
        widget=filters.widgets.BooleanWidget())
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug')

    def favorite_filter(self, queryset, name, value):
        return Recipe.objects.filter(favorite__user=self.request.user)

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'favourite', 'cart']
