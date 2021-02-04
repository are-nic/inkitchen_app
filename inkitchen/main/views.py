from django.shortcuts import render, redirect, reverse
from users.forms import UserRegistrationForm, UserLoginForm
from order.forms import PlanMenuForm
from food.models import Recipe


def index(request):
    """
    обработка на главной странице форм ввода email для продолженя регистрации,
    вывод группы рецептов для карусели,
    отправка форм логинга и регистрации для popup-окон,
    формы выбора плана питания
    Обработка плана меню для передачу в сессию, чтобы в корзине ограничить выбор кол-ва блюд в соответсвии с выбранным
    планом питания.
    """
    if request.method == 'POST':
        choose_plan_form = PlanMenuForm(request.POST)
        if choose_plan_form.is_valid():
            # присваиваем значение выбранного плана меню переменной
            plan = choose_plan_form.cleaned_data.get('plan_menu')
            request.session['plan_menu'] = plan  # передаем в сессию пользователя выбранный им план питания

            return redirect('recipes')
        # email = request.POST.get('email')                               # получение значения поля
        # return redirect(reverse('register'), {'email': email})          # перенаправление на страницу регистрации

    request.session['plan_menu'] = 4    # если план меню не выбран и пользователь попал на страницу выбора блюд

    register_form = UserRegistrationForm()          # передаем форму регистрации на главную страницу
    login_form = UserLoginForm                      # передаем форму логинга на главную страницу для popup-окна
    recipes = Recipe.objects.all()                  # передаем список рецептов на главную страницу
    plan = PlanMenuForm()                           # передаем форму выбора плана питания

    data = {
        'register_form': register_form,
        'recipes': recipes,
        'login_form': login_form,
        'choose_plan_form': plan,
    }
    return render(request, 'main/index.html', data)


def about(request):
    """вывод страницы "О нас"""
    return render(request, 'main/about.html')


