from django.db.models import Sum
from django.http import HttpResponse
from recipes.models import Cart, Ingredient, RecipeIngredient


def cart_down(request):
    cart = Cart.objects.filter(user=request.user)
    recipes = [item.recipe.id for item in cart]
    buy = RecipeIngredient.objects.filter(
        recipe__in=recipes
    ).values(
        'ingredient'
    ).annotate(
        amount=Sum('amount')
    )

    buy_list_text = 'Список покупок с сайта Foodgram:\n\n'
    for item in buy:
        ingredient = Ingredient.objects.get(pk=item['ingredient'])
        amount = item['amount']
        buy_list_text += (
            f'{ingredient.name}, {amount} '
            f'{ingredient.measurement_unit}\n'
        )

    response = HttpResponse(buy_list_text, content_type="text/plain")
    response['Content-Disposition'] = (
        'attachment; filename=shopping-list.txt'
    )

    return response
