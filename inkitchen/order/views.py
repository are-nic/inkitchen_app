from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .forms import OrderForm
from .models import OrderRecipe, Order
from django import forms

from geopy.geocoders import Nominatim


def order_create(request):
    cart = request.session.get('cart', {})              # получаем содержимое корзины из сессии

    if request.method == 'POST':
        form_order = OrderForm(request.POST)
        if form_order.is_valid():
            order = form_order.save(commit=False)
            order.owner = request.user                  # записываем в поле owner текущего пользователя
            order.save()                                # сохраняем в БД экземпляр заказа

            for recipe in cart:
                OrderRecipe(                            # создаем экземпляр продукта в заказе
                    order=order,
                    recipe=recipe['recipe'],
                    price=recipe['price'],
                    qty=recipe['qty']
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
    lat = request.GET.get('lat', None)      # получаем из шаблона широту
    lon = request.GET.get('lon', None)      # получаем из шаблона долготу
    geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                      "Chrome/53.0.2785.116 Safari/537.36")
    location = geolocator.reverse([lat, lon])   # преобразуем координаты в адрес (json формат)
    # address = location.address

    address = location.raw['address']
    # print(address)

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
    print(state, city, municipality, street, house)
    return JsonResponse(response)