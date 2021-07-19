from django import forms
from .models import Order
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

    ON_DELIVERY = 'on delivery'
    ONLINE = 'online'
    PAY_METHOD = (
        (ON_DELIVERY, 'Оплата наличными или банковской картой при получении'),
        (ONLINE, 'Онлайн оплата'),
    )
    pay_method = forms.ChoiceField(choices=PAY_METHOD, label='Оплата', initial=ONLINE, widget=forms.RadioSelect)

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
            }),
        }


class PlanMenuForm(forms.Form):
    """
    План меню для выбора количества блюд на главной странице по дням
    Формат получения даты изменен на "день недели, число месяц" ('%A, %d %b')
    """

    delivery_date = forms.DateField(widget=forms.DateInput(attrs={'readonly': 'readonly'}))      # дата заказа
    delivery_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'text',
                                                                  'class': 'bs-timepicker', }))  # время заказа
    qty_meals = forms.IntegerField(min_value=0, widget=forms.NumberInput)       # кол-во блюд на конкретный день заказа


PlanMenuFormSet = forms.formset_factory(PlanMenuForm, min_num=7, max_num=7, extra=0)