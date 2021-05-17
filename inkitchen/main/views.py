from django.shortcuts import render, redirect, reverse
from users.forms import UserRegistrationForm, UserLoginForm
from order.forms import PlanMenuForm, PlanMenuFormSet
from food.models import Recipe
from datetime import date, timedelta, time
import locale


def index(request):
    """
    обработка на главной странице форм ввода email для продолженя регистрации,
    вывод группы рецептов для карусели,
    отправка форм логинга и регистрации для popup-окон,
    формы выбора плана питания
    Обработка плана меню для передачу в сессию, чтобы в корзине ограничить выбор кол-ва блюд в соответсвии с выбранным
    планом питания.
    """

    locale.setlocale(locale.LC_ALL, ('en_EN', 'UTF-8'))     # для англ. названий дней недели и месяцев
    week_rus = {
        'monday': 'Понедельник',
        'tuesday': 'Вторник',
        'wednesday': 'Среда',
        'thursday': 'Четверг',
        'friday': 'Пятница',
        'saturday': 'Суббота',
        'sunday': 'Воскресенье',
    }

    if request.method == 'POST':
        menu_formset = PlanMenuFormSet(request.POST or None)
        if menu_formset.is_valid():
            # задаем пустой словарь ключу 'plan_menu' в сессии
            request.session['plan_menu'] = {}
            for data in menu_formset.cleaned_data:
                # переменая для обращения к дню недели
                week_day = data.get('delivery_date').strftime("%A").lower()
                # используем день недели как ключ для добавления словаря с данными плана-меню
                # т.к. данные формата datetime не сериализуются в json, превращаем их в строковый вид
                # отдельно добавляем параметр name_rus для отображения русских названий дней недели
                delivery_date = data.get('delivery_date').strftime('%d.%m.%Y')
                delivery_time = data.get('delivery_time').strftime('%H:%M')
                qty_meals = data.get('qty_meals')
                request.session['plan_menu'][week_day] = {'delivery_date': delivery_date,
                                                          'delivery_time': delivery_time,
                                                          'qty_meals': qty_meals,
                                                          'name_rus': week_rus[week_day]}

            next_day = (date.today() + timedelta(days=1)).strftime("%A").lower()    # завтрашний день недели
            return redirect('recipes/week/' + next_day)         # перенаправление на завтрашний день на стр. рецептов
        else:
            print('error data')

    # инициализируем список данных по умолчанию для 7 ближайших дней заказа в формсет выбора плана меню
    menu_formset = PlanMenuFormSet(initial=[
        {'delivery_date': date.today() + timedelta(days=day),
         'delivery_time': time(hour=5, minute=30).isoformat(timespec='minutes'),
         'qty_meals': 0} for day in range(1, 8)
    ])

    register_form = UserRegistrationForm()          # передаем форму регистрации на главную страницу
    login_form = UserLoginForm                      # передаем форму логинга на главную страницу для popup-окна
    recipes = Recipe.objects.all()                  # передаем список рецептов на главную страницу

    data = {
        'register_form': register_form,
        'recipes': recipes,
        'login_form': login_form,
        'menu_formset': menu_formset
    }
    return render(request, 'main/index.html', data)


def about(request):
    """вывод страницы "О нас"""
    return render(request, 'main/about.html')


