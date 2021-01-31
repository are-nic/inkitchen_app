from django.db import models
from food.models import Recipe, Product
from django.contrib.auth import get_user_model

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


class OrderItem(models.Model):

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='заказ')
    recipe = models.ForeignKey(Recipe, related_name='recipe_items', on_delete=models.CASCADE, verbose_name='рецепт')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name='продукт')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    qty = models.PositiveIntegerField(verbose_name='кол-во порций')

    class Meta:
        ordering = ('product',)
        verbose_name = 'Продукт заказа'
        verbose_name_plural = 'Продукты заказа'
        db_table = 'Order_Items'

    def __str__(self):
        return '{}'.format(self.product)

    def get_cost_item(self):
        """
        получить стоимость продукта в заказе (его цена * его кол-во)
        :return: стоимость продукта
        """
        return self.price * self.qty