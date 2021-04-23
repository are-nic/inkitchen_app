from django import forms
from .models import Order
from datetime import date, timedelta
import locale
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class OrderForm(forms.ModelForm, forms.Form):

    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-order',
        'placeholder': 'Город',
    }))
    street = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-order',
        'placeholder': 'Улица',
    }))
    building = forms.CharField(max_length=10, widget=forms.TextInput(attrs={
        'class': 'form-order',
        'placeholder': 'Дом',
    }))
    apartment = forms.IntegerField(required=False, min_value=1, widget=forms.NumberInput(attrs={
        'class': 'form-order',
        'placeholder': 'Квартира',
    }))

    class Meta:
        model = Order
        fields = ['name', 'address', 'phone_number', 'city', 'street', 'building', 'apartment', 'pay_method', 'at_door']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-order',
                'placeholder': 'Имя',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-order',
                'placeholder': 'Адрес',
            }),
            'phone_number': PhoneNumberPrefixWidget(attrs={
                'class': 'form-order',
                'placeholder': 'Телефон',
            }),
            'at_door': forms.CheckboxInput(attrs={
                'class': 'form-order',
                'placeholder': 'Оставить заказ у дверей',
            }),
        }


class PlanMenuForm(forms.Form):
    """
    План меню для выбора количества блюд на главной странице
    """
    locale.setlocale(locale.LC_ALL, "")             # для русских названий в датах
    start_day = date.today() + timedelta(days=1)    # начальная дата с завтрашнего дня
    end_day = start_day + timedelta(days=6)         # конечная дата = + 6 дней от завтрашней
    WEEK = {}
    delta = end_day - start_day
    key = 0
    for i in range(delta.days + 1):
        WEEK[key] = ((start_day + timedelta(i)).strftime('%A, %d %b'))
        key += 1
    key = 0

    delivery_date = forms.DateField()
    delivery_time = forms.TimeField()
    qty_meals = forms.NumberInput()
