from django.contrib import admin
from .models import *


class CategoryProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}                                       # для автозаполнения поля slug


class ProductMarketAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'available', 'created', 'updated']    # показываемые поля
    list_filter = ['available', 'created', 'updated']                               # фильтрация
    filter_horizontal = ('tags',)                                                   # выбор тэгов
    list_editable = ['price', 'stock', 'available']                                 # поля для быстрого редактирования


# Регистрация моделей в админке
admin.site.register(CategoryProduct, CategoryProductAdmin)
admin.site.register(ProductMarket, ProductMarketAdmin)
admin.site.register(OrderMarket)
admin.site.register(OrderItemMarket)
admin.site.register(ShippingAddress)