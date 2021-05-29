from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView
from rest_framework.generics import get_object_or_404

from .forms import RecipeForm, IngredientFormSet
from .models import Recipe


def delivery_day(request, index):
    """
    вывод плана меню на конкретный день на странице рецептов
    На страницу рецептов функция отдает: weekday - словарь с данными по конкретному дню недели
                                         plan_menu - словарь с данными по всем дням
                                         recipes - все рецепты из БД
    """
    plan_menu = request.session['plan_menu']        # получаем план-меню из сессии
    weekday_data = plan_menu[index]     # выделяем данные по конкретному дню, на странице которого находится покупатель
    recipes = Recipe.objects.all()
    cart = request.session.get('cart', {})  # получаем корзину из сессии
    qty_meals_added = len(cart[weekday_data['delivery_date']])  # определяем кол-во добавленных рецептов в конкретный день

    need_meals = 0
    for meal in plan_menu.values():
        need_meals += meal.get('qty_meals')
    print('need meals added:', need_meals)

    data = {
        'qty_meals_added': qty_meals_added,
        'weekday': weekday_data,
        'plan_menu': plan_menu,
        'recipes': recipes,
        'need_meals': need_meals,
    }
    print('----------------------------------------plan-menu-----------------------------------------')
    for day in plan_menu:
        print(day, plan_menu[day])

    return render(request, "recipes.html", data)


def all_recipes(request):   # УБРАТЬ
    """
    вывод всех рецептов на странице Рецептов
    Выборка из сессии плана-меню (даты, кол-ва блюд на конкретный день) и отправка в html-шаблон
    """
    plan_menu = request.session['plan_menu']
    recipes = Recipe.objects.all()                                  # получаем экземпляры всех рецептов
    data = {
        "recipes": recipes,
        "plan_menu": plan_menu
    }
    return render(request, "recipes.html", data)                    # выводим их на страницу рецептов


def get_ingredients(request):
    """
    получение id рецепта из ajax и отправка в скрипт данных об ингредиентах по конкретному рецепту
    """
    id = request.GET.get('id', None)    # получаем из ajax id рецепта
    recipe = Recipe.objects.get(id=id)  # получаем экземпляры всех рецептов
    ingredients = {}
    for ingredient in recipe.ingredients.all():
        ingredients[str(ingredient)] = [ingredient.qty, ingredient.get_unit_display()]
        print(ingredient, ingredient.qty, ingredient.get_unit_display())
    response = {
        'ingredients': ingredients,
    }
    return JsonResponse(response)


'''class RecipeDetailView(DetailView):
    """вывод рецепта на странице"""
    model = Recipe
    template_name = 'food/recipe_detail.html'
    context_object_name = 'recipe'   '''                 # имя 'recipe' для обращения в шаблоне к полям рецепта


@login_required(login_url='home')
def create_recipe(request):
    """
    создание рецепта
    если пользователь неавторизован, выкидывает на страницу рецептов
    """

    error = ''                                                  # переменная для сообщение об ошибке
    if request.method == 'POST':
        form_recipe = RecipeForm(request.POST, request.FILES)   # данные, полученные из формы создания рецепта
        if form_recipe.is_valid():                              # если данные из формы коректно заполнены
            recipe = form_recipe.save(commit=False)             # сохраняем данные формы без коммита в БД
            recipe.owner = request.user                         # присваиваем значению owner текущего пользователя
            formset = IngredientFormSet(request.POST, instance=recipe)
            if formset.is_valid():
                recipe.save()                                   # сохраняем рецепт в БД
                form_recipe.save_m2m()                          # сохраняем ингридиенты в БД
                formset.save()
                return redirect('recipes')                      # перенаправляем пользователя на страницу рецептов
        else:
            error = 'Введеные данные некорректны'

    form_recipe = RecipeForm()
    formset = IngredientFormSet()
    data = {
        'form_recipe': form_recipe,
        'formset': formset,
        'error': error,
    }
    return render(request, 'create_recipe.html', data)


@login_required(login_url='home')
def edit_recipe(request, id):
    """
    изменить существующий рецепт
    если пользователь неавторизован, выкидывает на страницу рецептов
    """
    recipe = get_object_or_404(Recipe, id=id)
    if recipe.owner != request.user:        # проверка на то, что текущий пользователь - создатель рецепта
        raise PermissionDenied

    form_recipe = RecipeForm(request.POST or None, request.FILES or None, instance=recipe)
    ingredients_formset = IngredientFormSet(request.POST or None, instance=recipe)
    if form_recipe.is_valid():
        recipe = form_recipe.save(commit=False)
        if ingredients_formset.is_valid():
            recipe.save()                   # сохраняем рецепт в БД
            form_recipe.save_m2m()          # сохраняем тэги в БД
            ingredients_formset.save()      # сохраняем ингридиенты в БД

        return redirect('profile', slug=recipe.slug)

    data = {
        'form_recipe': form_recipe,
        'ingredients_formset': ingredients_formset,
        'recipe': recipe
    }
    return render(request, 'edit_recipe.html', data)


@login_required(login_url='home')
def remove_recipe(request, id):
    """
    Удалить рецепт
    если пользователь неавторизован, выкидывает на страницу рецептов
    """
    recipe = get_object_or_404(Recipe, id=id)
    if recipe.owner != request.user:
        raise PermissionDenied

    recipe.delete()
    return redirect('recipes')
