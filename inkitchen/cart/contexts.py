# контекстный процессор, предоставляющий данные корзины во всех шаблонах при обращении к ним.

from django.shortcuts import get_object_or_404
from food.models import Recipe


def cart_contents(request):
    """
    Подсчет стоимости рецептов и кол-ва их порций, добавленных в корзину.
    Общая стоимость корзины складывается из стоимости всех рецептов в корзине и кол-ва их порций.
    """
    cart = request.session.get('cart', {})

    cart_items = {}         # список данных по каждому рецепту (id, q_portion, recipe)
    total = 0               # общая стоимость всего заказа
    recipe_count = 0        # общее количество рецептов в корзине

    for delivery_date in cart:                                      # перебираем все даты заказа в корзине
        cart_items[delivery_date] = []
        recipe_count += len(cart[delivery_date])                    # прибавляем ко-во блюд по каждой дате заказа
        for recipe_id, q_portion in cart[delivery_date].items():    # перебираем в каждой дате рецепты и кол-во порций
            recipe = get_object_or_404(Recipe, pk=recipe_id)        # получаем экземпляр рецепта, добавленый в корзину
            # если кол-во порций рецепта в сессии меньше 1, то ставим 1, чтобы случайно не было нулевых порций в заказе
            if q_portion < 1:
                q_portion = 1
            total += q_portion * recipe.price                       # общая цена заказа
            cart_items[delivery_date].append({
                'id': recipe_id,
                'recipe': recipe,
                'q_portion': q_portion,
            })
    print('----------------------------------contexts.py---------------------------------------------')
    for data in cart_items:
        print(data, cart_items[data])
    return {'cart_items': cart_items, 'total': total, 'recipe_count': recipe_count}