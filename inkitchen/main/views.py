from django.shortcuts import render


def index(request):
    """вывод главной страницы"""
    return render(request, 'main/index.html')


def about(request):
    """вывод страницы "О нас"""
    return render(request, 'main/about.html')
