from django.shortcuts import render, get_object_or_404
from .models import CategoryProduct, ProductMarket, OrderMarket, OrderItemMarket
from django.http import JsonResponse


def product_list(request, category_slug=None):
    """
    Вывод продуктов на странице
    По умолчанию запрос отфильтрован по available=True, чтобы получить только доступные продукты.
    Если в фуркцию поступит необязатльный параметр category_slug, то фильтрация продуктов осуществояется по категории.
    :param request:
    :param category_slug:
    :return:
    """
    category = None
    categories = CategoryProduct.objects.all()
    products = ProductMarket.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(CategoryProduct, slug=category_slug)
        products = products.filter(category=category)

    # ----------------------------------------------обработка корзины-------------------------------------------------
    if request.user.is_authenticated:
        customer = request.user
        order, created = OrderMarket.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitemmarket_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cart_items = order['get_cart_items']

    data = {
        'category': category,
        'categories': categories,
        'products': products
    }
    return render(request, 'products.html', data)


def update_item(request):
    """
    добавление продукта в корзину
    """
    return JsonResponse('Товар был добавлен', safe=False)