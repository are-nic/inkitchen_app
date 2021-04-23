from django.shortcuts import render, get_object_or_404
from .models import CategoryProduct, ProductMarket


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

    data = {
        'category': category,
        'categories': categories,
        'products': products
    }
    return render(request, 'products.html', data)


def cart(request):
    """
    Корзина
    """
    data = {}
    return render(request, 'products.html', data)


def checkout(request):
    """
    Заказ
    """
    data = {}
    return render(request, 'products.html', data)