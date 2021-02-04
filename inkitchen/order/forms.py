from django import forms
from .models import Order, OrderItem
from django.forms import Select, RadioSelect


class OrderItemForm(forms.ModelForm, forms.Form):
    class Meta:
        model = OrderItem
        fields = ['product', ]

        widgets = {
            'product': Select(attrs={
                'class': 'select-product',
                'style': 'width: 200px',
            }),
        }


class PlanMenuForm(forms.Form):
    """
    План меню для выбора количества блюд на главной странице
    """
    PLAN_MENU = (
        ('4', 4),
        ('6', 6),
        ('8', 8),
        ('10', 10)
    )

    plan_menu = forms.ChoiceField(choices=PLAN_MENU, widget=RadioSelect(attrs={'class': 'card-radio'}), initial='4')