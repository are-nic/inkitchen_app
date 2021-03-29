from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import TextInput, EmailInput, ModelForm, Textarea

User = get_user_model()


class UserLoginForm(forms.Form):
    """форма для входа пользователя на сайт"""
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class UserRegistrationForm(UserCreationForm):
    """
    форма для регистрации пользователя
    поле username скрыто и заполняется автоматически из 30 слуяайных букв латиницы
    регистрация осуществляется на основе email и password
    """

    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    CHOICES = (
        ('customers', 'Покупатель'),
        ('cooks', 'Повар'),
        ('doctors', 'Врач'),
        ('nutritionists', 'Диетолог'),
    )
    group = forms.ChoiceField(choices=CHOICES, label='Группа пользователя', widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'group']

        widgets = {
            'email': EmailInput(attrs={
                'placeholder': 'Введите E-mail',

            }),
            'password1': TextInput(attrs={
                'placeholder': 'введите пароль',
            }),
            'password2': TextInput(attrs={
                'placeholder': 'повторите пароль',
            }),
        }

    def clean_email(self):
        """ Валидация поля Email """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email):
            raise forms.ValidationError('Email должен быть уникальным')
        return email

    def clean_password2(self):
        """ Валидация полей Password """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password1 or not password2:
            raise ValidationError("Пароль не должен быть пустым")

        if password1 != password2:
            raise ValidationError("Пароли не совпадают")

        return password2


class UserProfileForm(ModelForm, forms.Form):
    """форма для зменения данных пользователя в ЛК"""
    class Meta:
        model = User
        fields = ['first_name', 'email', 'phone', 'address', 'about']

        widgets = {
            'first_name': TextInput(attrs={
                'placeholder': 'Введите имя',
            }),
            'email': EmailInput(attrs={
                'placeholder': 'Введите email',
            }),
            'phone': TextInput(attrs={
                'placeholder': 'Введите номер телефона',
            }),
            'address': TextInput(attrs={
                'placeholder': 'Введите адрес',
            }),
            'about': Textarea(attrs={
                'placeholder': 'О себе',
            }),
        }