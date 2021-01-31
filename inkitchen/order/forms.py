from django import forms
from .models import Order, OrderItem


class OrderItemForm(forms.ModelForm, forms.Form):
    class Meta:
        model = OrderItem
        fields = ['product', ]

        widgets = {
            'product': forms.RadioSelect(attrs={
                'class': 'select-product',
            }),
        }