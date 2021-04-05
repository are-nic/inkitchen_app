from django import forms
from .models import Order
from django.forms import RadioSelect
from datetime import date, timedelta
import locale


class OrderForm(forms.ModelForm, forms.Form):
    class Meta:
        model = Order
        fields = []


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

    week = forms.ChoiceField(choices=WEEK, widget=RadioSelect(attrs={'class': 'card-radio'}))