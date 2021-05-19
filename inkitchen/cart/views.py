from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib import messages


def cart_add(request, id):  # УБРАТЬ
    """
    Добавление блюда в корзину
    """
    cart = request.session.get('cart', {})
    quantity = 1  # добавляем одну порцию блюда в корзину
    cart[id] = cart.get(id, quantity)

    request.session['cart'] = cart

    return redirect(reverse('recipes'))  # после добавления рецепта в корзину возврат к списку рецептов


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
        quantity = cart[delivery_date][recipe_id] + 1       # увеличиваем имеющееся кол-во порций юлюда в корзине на 1
        cart[delivery_date][recipe_id] = quantity

    cart[delivery_date][recipe_id] = cart.get(recipe_id, quantity)

    request.session['cart'] = cart                  # обновляем корзину с учетом изменений
    # messages.error(request, 'Корзина полна, замените рецепт или выберите другой план питания')
    return HttpResponse("рецепт добавлен")


def adjust_cart(request):
    """
    Регулировать кол-во блюд внутри корзины
    """
    cart = request.session.get('cart', {})
    recipe_id = request.GET.get('recipe_id', None)
    delivery_date = request.GET.get('delivery_date', None)
    quantity = int(request.GET.get('quantity', None))

    if request.GET.get('quantity_plus'):            # если была нажата кнопка "+" - увеличение кол-ва порций
        cart[delivery_date][recipe_id] += 1         # добавляем 1 к кол-ву порций конкретного рецепта в корзине
    elif request.GET.get('quantity_minus'):         # если была нажата кнопка "-" - уменьшение кол-ва порций
        cart[delivery_date][recipe_id] -= 1         # отнимаем 1 от кол-ва порций конкретного рецепта в корзине
    elif quantity <= 0:                             # если кол-во порций рецепта в корзине <= 0...
        cart[delivery_date].pop(recipe_id)          # ...удаляем выбранный рецепт из корзины в сессии

    request.session['cart'] = cart
    return HttpResponse("корзина изменена")


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
    return HttpResponse("рецепт удален")