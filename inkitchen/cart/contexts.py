# контекстный процессор, предоставляющий данные корзины во всех шаблонах при обращении к ним.

from django.shortcuts import get_object_or_404
from food.models import Recipe


def cart_contents(request):
    """
    Подсчет стоимости рецептов и количества их порций.
    Общая стоимость корзины складывается из стоимости всех рецептов в корзине и количества их порций.
    Обеспечивает доступность кол-ва порций блюд в корзине в для navbar (не используется)
    """
    cart = request.session.get('cart', {})

    cart_items = []         # список данных по каждому рецепту (id, q_portion, recipe)
    total = 0               # общая стоимость всего заказа
    recipe_count = 0        # общее количество рецептов

    for delivery_date in cart:                                      # перебираем все даты заказа в корзине
        for recipe_id, q_portion in cart[delivery_date].items():    # перебираем в каждой дате
            recipe = get_object_or_404(Recipe, pk=recipe_id)        # получаем экземпляр рецепта, добавленый в корзину
            total += q_portion * recipe.price                       # общая цена заказа
            recipe_count += q_portion                               # кол-во в навбаре в пункте Корзина (не исп.)
            cart_items.append({
                'id': recipe_id,
                'q_portion': q_portion,
                'recipe': recipe,
            })
            print(cart_items)
    
    return {'cart_items': cart_items, 'total': total, 'recipe_count': recipe_count}