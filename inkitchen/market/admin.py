from django.contrib import admin
from .models import *


class OrderItemMarketInline(admin.TabularInline):
    model = OrderItemMarket
    raw_id_fields = ['product']


@admin.register(OrderMarket)
class OrderMarketAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'date_order', 'complete', 'transaction_id']
    inlines = [OrderItemMarketInline, ]


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
admin.site.register(ShippingAddress)