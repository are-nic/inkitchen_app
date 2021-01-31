from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}   # для автозаполнения поля slug у модели Category


class IngredientOfRecipeAdmin(admin.TabularInline):
    model = IngredientOfRecipe


class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)               # выбор тэгов
    inlines = [IngredientOfRecipeAdmin, ]


class ProductAdmin(admin.ModelAdmin):
    # поля для вывода в панели админа
    list_display = ['name', 'qty_per_item', 'unit', 'stock', 'price', 'shop', 'available']
    list_filter = ['tag']                                                   # фильтр по тэгу
    # list_editable = ['price', 'stock', 'unit', 'available']               # поля для быстрого редактирования


# Регистрация моделей в админке
admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(TagRecipe)
admin.site.register(TagIngredient)
admin.site.register(Shop)




