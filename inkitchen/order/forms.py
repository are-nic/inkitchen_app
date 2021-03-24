from django import forms
from .models import Order, OrderItem
from django.forms import Select, RadioSelect
from food.models import Product, IngredientOfRecipe


class OrderForm(forms.ModelForm, forms.Form):
    class Meta:
        model = Order
        fields = []


class OrderItemForm(forms.ModelForm, forms.Form):

    def __init__(self, ingredient, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(tag=ingredient)

    class Meta:
        model = OrderItem
        fields = ['product', ]

        widgets = {
            'product': Select(attrs={
                'class': 'select-product',
                'style': 'width: 300px',
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