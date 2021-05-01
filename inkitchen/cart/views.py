from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib import messages


def cart_add(request, id):
    """
    Добавление блюда в корзину
    """
    cart = request.session.get('cart', {})
    # получаем из сессии значение выбранного кол-во блюд (план питания)
    # plan_menu = int(request.session.get('plan_menu'))
    # if len(cart) < plan_menu:  # если количество рецептов в корзине меньше числа блюд по плану меню
    # quantity = int(request.POST.get('quantity'))  # получаем кол-во блюд при добалвении блюда в корзину
    quantity = 1  # добавляем одну порцию блюда в корзину
    cart[id] = cart.get(id, quantity)

    request.session['cart'] = cart
    # else:
    # messages.error(request, 'Корзина полна, замените рецепт или выберите другой план питания')

    return redirect(reverse('recipes'))  # после добавления рецепта в корзину возврат к списку рецептов


@login_required(login_url='home')
def add_to_cart(request):
    """
    Добавление 1 блюда в корзину при нажатии на кнопку "+" на странице рецептов с помощью AJAX.
    Данные передаются в функцию, которая проверят: было ли добавлено блюдо в корзину ранее или впервые.
    В первом случае к имеющемуся кол-ву порций прибавляется 1. Во втором случае кол-во порций устанавливается = 1
    """
    recipe_id = request.GET.get('recipe_id', None)  # получаем из ajax id добавленного в корзину рецепта

    cart = request.session.get('cart', {})

    # проверяем, есть ли рецепт в корзине (в сессии)
    if recipe_id not in cart:                       # если рецепта нет в корзине, то кол-во порций устанавливаем = 1
        quantity = 1
        cart[recipe_id] = quantity                  # заносим в сессию кол-во порций данного блюда
    else:                                           # если на момент добавления блюда, оно уже в корзине
        quantity = cart[recipe_id] + 1              # увеличиваем имеющееся кол-во порций юлюда в корзине на 1
        cart[recipe_id] = quantity

    cart[recipe_id] = cart.get(recipe_id, quantity)

    request.session['cart'] = cart

    return HttpResponse("рецепт добавлен")


def adjust_cart(request, id):
    """
    Отрегулировать кол-во блюд внутри корзины
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
    Удалить блюдо из корзины
    """
    cart = request.session.get('cart', {})
    cart.pop(id)
    request.session['cart'] = cart
    return redirect(reverse('recipes'))