from django import forms
from .models import Order, OrderItem


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['plan_menu']


class OrderItemForm(forms.ModelForm, forms.Form):
    class Meta:
        model = OrderItem
        fields = '__all__'


ProductFormSet = forms.inlineformset_factory(Order, OrderItem, form=OrderItemForm, can_delete=True, fields=('product',),
                                             max_num=1, min_num=1, extra=0, fk_name='order',
                                             widgets={
                                                    'product': forms.Select(attrs={
                                                        'style': 'width: 250px',
                                                    }),
                                             })