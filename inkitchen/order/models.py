from django.db import models
from food.models import Recipe
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta


User = get_user_model()


class Order(models.Model):                      # заказ

    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='Покупатель')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменен')
    paid = models.BooleanField(default=False, verbose_name='Оплачен')

    class Meta:
        ordering = ('updated_at',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        db_table = 'Order'

    def __str__(self):
        return 'Заказ от: {}'.format(self.owner.email)

    def get_total_cost(self):
        """
        Получить полную стоимость заказа
        :return: сумму всех продуктов
        """
        return sum(item.get_cost() for item in self.items.all())


class OrderRecipe(models.Model):

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    recipe = models.ForeignKey(Recipe, related_name='recipe_items', on_delete=models.CASCADE, verbose_name='Рецепт')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    qty = models.PositiveIntegerField(verbose_name='Кол-во порций')
    delivery_datetime = models.DateTimeField(verbose_name='Дата и время доставки',
                                             default=datetime.today() + timedelta(days=1))

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Рецепт заказа'
        verbose_name_plural = 'Рецепты заказа'
        db_table = 'Order_Recipes'

    def __str__(self):
        return '{}'.format(self.recipe)

    def get_cost_item(self):
        """
        получить стоимость продукта в заказе (его цена * его кол-во)
        :return: стоимость продукта
        """
        return self.price * self.qty