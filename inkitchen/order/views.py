from django.shortcuts import render, get_object_or_404
from .forms import OrderItemForm, OrderForm
from food.models import Recipe, Product
from .models import OrderItem, Order
from django import forms


def order_create(request):
    cart = request.session.get('cart', {})
    ingredients = 0
    for recipe_id in cart:
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        ingredients += recipe.ingredients.all().count()

    ProductFormSet = forms.inlineformset_factory(Order, OrderItem, form=OrderItemForm, fields=('product',),
                                                 max_num=100, min_num=0, extra=ingredients)

    if request.method == 'POST':
        form_order = OrderForm(request.POST)
        if form_order.is_valid():
            order = form_order.save(commit=False)
            order.owner = request.user      # записываем в поле owner текущего пользователя
            order.save()                    # сохраняем в БД экземпляр заказа

            formset = ProductFormSet(request.POST, instance=order)
            for product in formset:
                product(price=)
            print(formset)
            if formset.is_valid():                         # сохраняем ингридиенты в БД
                formset.save()

                ''' for recipe_id in cart:
                recipe = get_object_or_404(Recipe, pk=recipe_id)    # получаем рецепт по id из корзины
                ingredients = recipe.ingredients.all()              # получаем все игредиенты текущего рецепта
                for ingredient in ingredients:                      # перебираем ингридиенты рецепта
                    product_form = OrderItemForm(request.POST)
                    product_name = product_form.save(commit=False)
                    product = Product.objects.get(name=product_name)

                    order_item = OrderItem(
                        order=order,
                        recipe=recipe,
                        product=product,
                        price=product.price,
                        qty=ingredient.qty
                    )
                    order_item.save()'''

                cart.clear()                                        # очистка корзины
                return render(request, 'order/order_created.html')

    product_formset = ProductFormSet()

    data = {
        'product_formset': product_formset,
        'cart': cart,
    }
    return render(request, 'order/order_create.html', data)