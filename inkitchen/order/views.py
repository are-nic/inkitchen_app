from django.shortcuts import render, get_object_or_404
from .forms import OrderItemForm, OrderForm
from food.models import Recipe, Product
from .models import OrderItem, Order
from django import forms


def order_create(request):
    cart = request.session.get('cart', {})      # получаем содержимое корзины из сессии

    # считаем кол-во ингридиентов во всех рецептах корзины
    ingredients_count = 0
    initial_ingred = []
    for recipe_id in cart:
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        ingredients_count += recipe.ingredients.all().count()
        ingredients = recipe.ingredients.all()
        for ingredient in ingredients:
            initial_ingred.append(list(Product.objects.filter(tag=ingredient.name).values('name')))
            #print(list(Product.objects.filter(tag=ingredient.name).values('name')))
    print(initial_ingred)

    # в extra передаем общее число всех ингридиентов корзины для вывода соответсвующего кол-ва форм
    ProductFormSet = forms.formset_factory(form=OrderItemForm, min_num=0, extra=ingredients_count)

    if request.method == 'POST':
        form_order = OrderForm(request.POST)
        if form_order.is_valid():
            order = form_order.save(commit=False)
            order.owner = request.user      # записываем в поле owner текущего пользователя
            order.save()                    # сохраняем в БД экземпляр заказа

            # собираем выбранные продукты из форм
            product_list = []
            formset = ProductFormSet(request.POST, form_kwargs={'ingredient': 1})
            if formset.is_valid():
                for form in formset:
                    #print(form.cleaned_data['product'])
                    product_list.append(form.cleaned_data['product'])    # заносим выбранные продукты в список
            print('-------------------------------------------------------')
            product_order_set = []                                      # набор продуктов заказа
            product_index = 0
            for recipe_id in cart:
                recipe = get_object_or_404(Recipe, pk=recipe_id)        # получаем рецепт по id из корзины
                ingredients = recipe.ingredients.all()                  # получаем все игредиенты текущего рецепта
                for ingredient in ingredients:                          # перебираем ингридиенты рецепта
                    product = Product.objects.get(name=product_list[product_index])
                    #print(product)
                    order_item = OrderItem(                             # создаем экземпляр продукта в заказе
                        order=order,
                        recipe=recipe,
                        product=product,
                        price=product.price,
                        qty=ingredient.qty
                    )

                    product_order_set.append(order_item)
                    product_index += 1

            for product in product_order_set:
                product.save()

            cart.clear()                                            # очистка корзины
            return render(request, 'order/order_created.html')

    product_formset = ProductFormSet(form_kwargs={'ingredient': 1})

    data = {
        'product_formset': product_formset,
        'cart': cart,
    }
    return render(request, 'order/order_create.html', data)