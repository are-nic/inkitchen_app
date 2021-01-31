from django.shortcuts import render, redirect, reverse


def cart_detail(request):
    """
    Отображает страницу содержимого корзины
    """
    return render(request, "cart/cart.html")


def cart_add(request, id):
    """
    Добавление указанного количества товара в корзину
    """
    quantity = int(request.POST.get('quantity'))

    cart = request.session.get('cart', {})
    cart[id] = cart.get(id, quantity)

    request.session['cart'] = cart
    return redirect(reverse('recipes'))     # после добавления рецепта в корзину возврат к списку рецептов


def adjust_cart(request, id):
    """
    Отрегулировать кол-во продукта внутри корзины
    """
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[id] = quantity
    else:
        cart.pop(id)

    request.session['cart'] = cart
    return redirect(reverse('recipes'))


def remove_recipe_from_cart(request, id):
    """
    Удалить рецепт из корзины
    """
    cart = request.session.get('cart', {})
    cart.pop(id)
    request.session['cart'] = cart
    return redirect(reverse('recipes'))