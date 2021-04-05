from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}   # для автозаполнения поля slug у модели Category


class IngredientAdmin(admin.TabularInline):
    model = Ingredient


class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)               # выбор тэгов
    inlines = [IngredientAdmin, ]


# Регистрация моделей в админке
admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(TagRecipe)
admin.site.register(TagProduct)




