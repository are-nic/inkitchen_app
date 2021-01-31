from django.shortcuts import render, get_object_or_404
from .forms import OrderItemForm
from food.models import Recipe
from .models import OrderItem, Order


def order_create(request):
    '''
        if request.method == 'POST':
            form_order = OrderCreateForm(request.POST)
            if form_order.is_valid():
                order = form_order.save(commit=False)
                order.owner = request.user
                order.save()
    '''
    order = Order.objects.create(
        owner=request.user,
    )
    order.save()
    cart = request.session.get('cart', {})
    for id, quantity in cart.items():
        recipe = get_object_or_404(Recipe, pk=id)   # получаем рецепт по id из корзины
        ingredients = recipe.ingredients.all()      # получаем все игредиенты текущего рецепта
        for ingredient in ingredients:
            product_form = OrderItemForm(request.POST or None, instance=ingredient.name)
            product = product_form.save()
            order_item = OrderItem(
                order=order,
                recipe=recipe,
                product=product,
                qty=ingredient.qty
            )
            order_item.save()

        # очистка корзины
        cart.clear()
        return render(request, 'order_created.html')

    product_form = OrderItemForm

    data = {
        'cart': cart,
        'product_form': product_form,
    }
    return render(request, 'cart/cart.html', data)
