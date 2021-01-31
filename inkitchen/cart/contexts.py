from django.shortcuts import get_object_or_404
from food.models import Recipe, Product


def cart_contents(request):
    """
    Подсчет стоимости рецептов и количества их порций и ингридиентов.
    Общая стоимость рецептов складывается из стоимости первого продукта в списке ингридиента, кол-ва ингридиентов
    и количества порций.
    Обеспечивает доступность содержимого корзины в navbar при рендеринге каждой страницы
    """
    cart = request.session.get('cart', {})

    cart_items = []         # список данных по каждому рецепту (id, q_portion, recipe, recipe_price)
    total = 0               # общая стоимость всего заказа
    recipe_count = 0        # общее количество рецептов
    
    for id, q_portion in cart.items():
        recipe_price = 0                           # стоимость каждого рецепта в корзине исходя из стоимости инридиентов
        recipe = get_object_or_404(Recipe, pk=id)   # получаем экземпляр рецепта, кот. добавляем в корзину
        ingredients = recipe.ingredients.all()      # получаем все игредиенты текущего рецепта
        for ingredient in ingredients:
            # цена рецепта
            recipe_price += q_portion * ingredient.qty * Product.objects.filter(tag=ingredient.name.id)[0].price

            # общая цена
            total += q_portion * ingredient.qty * Product.objects.filter(tag=ingredient.name.id)[0].price
        recipe_count += q_portion
        cart_items.append({
            'id': id,
            'q_portion': q_portion,
            'recipe': recipe,
            'recipe_price': recipe_price
        })
    
    return {'cart_items': cart_items, 'total': total, 'recipe_count': recipe_count}