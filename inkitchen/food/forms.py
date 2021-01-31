from .models import Recipe, IngredientOfRecipe
from django import forms
from django.forms import (ModelForm,
                          TextInput,
                          Textarea,
                          Select,
                          FileInput,
                          CheckboxSelectMultiple,
                          NumberInput,
                          RadioSelect
                          )


class RecipeForm(ModelForm, forms.Form):
    """форма добавления рецепта"""

    CHOICES = (('OFFICE', 'Офиса'), ('HOME', 'Дома'),)
    group = forms.ChoiceField(choices=CHOICES, label='Группа рецепта', widget=forms.RadioSelect, initial='HOME')

    class Meta:
        model = Recipe
        fields = ['category', 'title', 'description', 'cooking_time', 'image', 'group', 'tags']

        # типы полей и их аттрибуты
        widgets = {
            'category': Select(attrs={
                'class': 'form-recipe-category form-control',
            }),
            'title': TextInput(attrs={
                'class': 'form-recipe-title form-control',
                'placeholder': 'Название рецепта',
            }),
            'description': Textarea(attrs={
                'class': 'form-recipe-title form-control',
                'placeholder': 'Описание рецепта',
            }),
            'cooking_time': TextInput(attrs={
                'class': 'form-recipe-cook-time form-control',
                'placeholder': 'Время приготовления',
            }),
            'image': FileInput(attrs={
                'class': 'form-recipe-image',
            }),
            'group': RadioSelect(attrs={
                'class': 'form-recipe-group',
            }),
            'tags': CheckboxSelectMultiple(attrs={
                'class': 'form-recipe-tags',
                'placeholder': 'Тэги',
            }),
        }


class IngredientForm(ModelForm, forms.Form):
    class Meta:
        model = IngredientOfRecipe
        fields = '__all__'


IngredientFormSet = forms.inlineformset_factory(Recipe, IngredientOfRecipe, form=IngredientForm, can_delete=True,
                                                fields=('name', 'qty', 'unit'), max_num=20, min_num=1, extra=0,
                                                fk_name='recipe',
                                                widgets={
                                                    'name': Select(attrs={
                                                        'class': 'form-recipe-ingredient form-control',
                                                        'placeholder': 'Выбрать ингредиент',
                                                        'style': 'width: 250px',
                                                    }),
                                                    'qty': NumberInput(attrs={
                                                        'class': 'form-recipe-ingredient-qty form-control',
                                                        'placeholder': 'Кол-во',
                                                        'style': 'width: 100px',
                                                    }),
                                                    'unit': Select(attrs={
                                                        'class': 'form-recipe-ingredient-unit form-control',
                                                        'placeholder': 'Ед.',
                                                        'style': 'width: 70px',
                                                    }),
                                                })
