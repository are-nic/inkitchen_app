# контекстный процессор, предоставляющий данные корзины во всех шаблонах при обращении к ним.

from django.shortcuts import get_object_or_404
from food.models import Recipe


def cart_contents(request):
    """
    Подсчет стоимости рецептов и количества их порций.
    Общая стоимость рецептов складывается из стоимости всех рецептов в корзине и количества порций.
    Обеспечивает доступность кол-ва порций блюд корзины в navbar
    """
    cart = request.session.get('cart', {})

    cart_items = []         # список данных по каждому рецепту (id, q_portion, recipe)
    total = 0               # общая стоимость всего заказа
    recipe_count = 0        # общее количество рецептов
    
    for id, q_portion in cart.items():
        recipe = get_object_or_404(Recipe, pk=id)   # получаем экземпляр рецепта, добавленый в корзину
        total += q_portion * recipe.price           # цена заказа
        recipe_count += q_portion                   # значение для отображения в навбаре в пункте Корзина
        cart_items.append({
            'id': id,
            'q_portion': q_portion,
            'recipe': recipe,
        })
    
    return {'cart_items': cart_items, 'total': total, 'recipe_count': recipe_count}