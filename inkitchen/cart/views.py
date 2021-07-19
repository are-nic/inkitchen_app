from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib import messages


def add_to_cart(request):
    """
    Добавление 1 блюда в корзину при нажатии на кнопку "+" на странице рецептов с помощью AJAX.
    Данные передаются в функцию, которая проверят: было ли добавлено блюдо в корзину ранее или впервые.
    В первом случае к имеющемуся кол-ву порций прибавляется 1. Во втором случае кол-во порций устанавливается = 1
    """
    recipe_id = request.GET.get('recipe_id', None)          # получаем из ajax id добавленного в корзину рецепта
    delivery_date = request.GET.get('delivery_date', None)  # получаем из ajax дату заказа

    cart = request.session.get('cart', {})
    if delivery_date not in cart:                           # если дата заказа еще не была в корзине,
        cart[delivery_date] = {}                            # то заводим для нее пустой словарь
    # проверяем, есть ли рецепт в корзине (в сессии) по конкретной дате заказа
    if recipe_id not in cart[delivery_date]:           # если рецепта нет в корзине, то кол-во порций устанавливаем = 1
        quantity = 1
        cart[delivery_date][recipe_id] = quantity           # заносим в сессию кол-во порций данного блюда
    else:                                                   # если на момент добавления блюда, оно уже в корзине
        quantity = cart[delivery_date][recipe_id] + 1       # увеличиваем имеющееся кол-во порций блюда в корзине на 1
        cart[delivery_date][recipe_id] = quantity

    cart[delivery_date][recipe_id] = cart.get(recipe_id, quantity)

    request.session['cart'] = cart                  # обновляем корзину с учетом изменений
    # messages.error(request, 'Корзина полна, замените рецепт или выберите другой план питания')
    return HttpResponse("Recipe was added")


def adjust_cart(request):
    """
    Регулировать кол-во блюд внутри корзины
    Из Ajax получаем данные о содержимом корзины: рецепты, даты доставки, кол-во порций, а так же логическое True
    той кнопки ( + или - ), которая была нажата в корзине на кол-ве порций рецепта.
    В зависимости от нажатой кнопки, уведичиваем или уменьшаем кол-во порций рецепта и обновляем корзину в сессии.
    """
    cart = request.session.get('cart', {})
    recipe_id = request.GET.get('recipe_id', None)
    delivery_date = request.GET.get('delivery_date', None)
    quantity = int(request.GET.get('quantity', None))

    # если была нажата кнопка "+" (увеличение кол-ва порций) и текущее кол-во порций рецепта меньше 99
    if request.GET.get('quantity_plus') and quantity < 99:
        cart[delivery_date][recipe_id] += 1                 # добавляем 1 к кол-ву порций конкретного рецепта в корзине
    # если была нажата кнопка "-" (уменьшение кол-ва порций) и текущее кол-во порций рецепта больше 0
    # Проверка - больше 0, т.к. из ajax приходит текущее (уменьшенное на 1) кол-во порций.
    elif request.GET.get('quantity_minus') and quantity > 0:
        cart[delivery_date][recipe_id] -= 1                 # отнимаем 1 от кол-ва порций конкретного рецепта в корзине

    request.session['cart'] = cart
    return HttpResponse("Cart was changed")


def remove_from_cart(request):
    """
    Удалить блюдо из корзины
    """
    cart = request.session.get('cart', {})

    recipe_id = request.GET.get('recipe_id', None)
    delivery_date = request.GET.get('delivery_date', None)

    cart[delivery_date].pop(recipe_id)

    # if len(cart[delivery_date]) == 0:       # если кол-во рецептов в конкретной дате корзины = 0
    #    cart.pop(delivery_date)             # удаляем эту дату из корзины сессии

    request.session['cart'] = cart
    return HttpResponse("Recipe was removed")