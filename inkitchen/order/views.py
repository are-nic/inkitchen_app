from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .forms import OrderForm, PlanMenuFormSet
from .models import OrderRecipe, Order
from food.models import Recipe
from django import forms
from datetime import datetime
import locale

from geopy.geocoders import Nominatim


def order_create(request):
    cart = request.session.get('cart', {})              # получаем содержимое корзины из сессии
    plan_menu = request.session['plan_menu']            # получаем план-меню из сессии
    delivery_time = ''
    if request.method == 'POST':
        form_order = OrderForm(request.POST)
        if form_order.is_valid():
            order = form_order.save(commit=False)
            order.customer = request.user               # записываем в поле customer текущего пользователя
            order.save()                                # сохраняем в БД экземпляр заказа

            for delivery_date in cart:                  # перебираем все дни заказа в корзине сессии
                if len(cart[delivery_date]) > 0:        # если на день заказа есть блюда (словарь дня заказа не пуст)
                    for data in plan_menu:              # перебираем все данные плана-меню сессии по дням
                        if plan_menu[data]['delivery_date'] == delivery_date:   # когда находим дату в плане меню
                            delivery_time = plan_menu[data]['delivery_time']    # забираем из плана-меню время доставки

                            # переводим дату и время в формат datetime вида ДД.ММ.ГГГГ ЧЧ:ММ и...
                            # ...принудительно завершаем цикл
                            delivery_datetime = datetime.strptime(delivery_date + ' ' + delivery_time, '%d.%m.%Y %H:%M')
                            break
                    # перебираем словарь каждого непустого дня заказа
                    for recipe_id, qty in cart[delivery_date].items():
                        OrderRecipe.objects.create(                    # создаем экземпляр рецепта для заказа
                            order=order,
                            recipe=Recipe.objects.get(id=recipe_id),
                            price=Recipe.objects.get(id=recipe_id).price,
                            qty=qty,
                            delivery_datetime=delivery_datetime
                        )

            cart.clear()                                            # очистка корзины
            return render(request, 'order/order_created.html')

    form = OrderForm()

    data = {
        'form': form,
        'cart': cart,
    }
    return render(request, 'order/order_create.html', data)


def get_current_location(request):
    """
    получить текущее местоположение пользователя при заказе
    в функцию передаются долгота и широта, возвращается адресс.
    """
    lat = request.GET.get('lat', None)      # получаем из ajax широту
    lon = request.GET.get('lon', None)      # получаем из ajax долготу
    geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                      "Chrome/53.0.2785.116 Safari/537.36")
    location = geolocator.reverse([lat, lon])   # преобразуем координаты в адрес (json формат)
    # address = location.address

    address = location.raw['address']

    town = address.get('town', '')
    city = address.get('city', '')
    municipality = address.get('municipality', '')
    state = address.get('state', '')
    street = address.get('road', '')
    house = address.get('house_number', '')
    if town == '':
        town = city
    if city == '':
        city = town

    response = {                              # создаем объект с данными для возврата в шаблон
        'town': town,
        'city': city,
        'municipality': municipality,
        'state': state,
        'street': street,
        'house': house
    }
    return JsonResponse(response)
