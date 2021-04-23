from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages, auth
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from food.models import Recipe

User = get_user_model()


def login(request):
    """обработка данных из формы входа на сайт"""
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(email=request.POST['email'], password=request.POST['password'])
            if user:
                auth.login(request, user)
                messages.success(request, "Вы вошли в свой аккаунт")

                if request.GET and request.GET['next'] != '':
                    next = request.GET['next']
                    return HttpResponseRedirect(next)
                else:
                    return redirect(reverse('home'))
            else:
                login_form.add_error(None, "Ваш Email или пароль неверны")
        messages.error(request, 'Ошибка введенных данных')
    else:
        login_form = UserLoginForm()

    data = {'login_form': login_form, 'next': request.GET.get('next', '')}
    return render(request, 'login.html', data)


def logout(request):
    """обработка выхода из акк"""
    auth.logout(request)
    messages.success(request, 'Вы вышли из своего аккаунта')
    return redirect(reverse('home'))


@login_required(login_url='home')
def profile(request):
    """обработка вывода страницы профиля пользователя"""

    recipes = Recipe.objects.filter(owner=request.user)

    return render(request, 'profile.html', {'recipes': recipes})


def register(request):
    """
    обработка данных из формы регистрации пользователя
    """
    if request.method == 'POST':
        data = request.POST
        register_form = UserRegistrationForm(data)
        if register_form.is_valid():
            new_user = register_form.save(commit=False)
            new_user.save()
            if request.POST.get("group") == 'cooks':                        # если пользователь выбрал категорию "Повар"
                new_user.groups.add(Group.objects.get(name='cooks'))        # добавим пользователя в группу cooks

            elif request.POST.get("group") == 'doctors':
                new_user.groups.add(Group.objects.get(name='doctors'))          # в группу doctors

            elif request.POST.get("group") == 'nutritionists':
                new_user.groups.add(Group.objects.get(name='nutritionists'))    # в группу nutritionists

            else:                                                       # если не выбрал категорию или выбрал customers
                new_user.groups.add(Group.objects.get(name='customers'))        # в группу customers

            user = auth.authenticate(request.POST.get('email'), password=request.POST.get('password1'))

            if user:
                auth.login(request, user)
                messages.success(request, "Вы успешно зарегистрированы")
                return redirect(reverse('home'))

            else:
                messages.error(request, "Невозможно войти в систему... ошибка данных")
    else:
        register_form = UserRegistrationForm()

    data = {'register_form': register_form}
    return render(request, 'register.html', data)


def validate_email(request):
    """Проверка доступности емайл при регистрации"""
    email = request.GET.get('email', None)
    response = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(response)


@login_required(login_url='home')
def profile_view(request, user_id):
    """
    Просмотр Личного кабинета любого пользователя. Доступно только для зарегистрированных Юзеров.
    Отбрасывает неавторизованых пользователей на главную страницу при попытке пройти по пути вручную

    :param request:
    :param user_id: id пользователя
    :return: страница пользователя с данными о нем и его рецептах
    """
    user = get_object_or_404(User, id=user_id)
    recipes = Recipe.objects.filter(owner=user)

    data = {
        'user': user,
        'recipes': recipes,
    }
    return render(request, 'profile.html', data)


@login_required(login_url='home')
def upgrade_profile(request, user_id):
    """
    Изменить данные пользователя в ЛК

    :param request:
    :param user_id: id пользователя
    :return: страница ЛК пользователя
    """
    user = get_object_or_404(User, id=user_id)
    if user != request.user:            # проверка на то, что текущий пользователь правит свой аккаунт
        raise PermissionDenied

    profile_form = UserProfileForm(request.POST or None, instance=user)

    if profile_form.is_valid():
        profile_form.save()
        return redirect('profile')

    data = {
        'profile_form': profile_form,
    }
    return render(request, 'upgrade_profile.html', data)


@login_required(login_url='home')
def remove_profile(request, user_id):
    """
    Удалить пользователя
    """
    user = get_object_or_404(User, id=user_id)
    if user != request.user:
        raise PermissionDenied

    user.delete()
    return redirect('home')
