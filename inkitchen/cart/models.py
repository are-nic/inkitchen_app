'''
class CartRecipe(models.Model):     # Рецепт в корзине

    user = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина',
                             related_name='related_recipe',
                             on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, verbose_name='Рецепт', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(verbose_name='Количество', default=1)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая цена')

    class Meta:
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Рецепты в корзине'
        db_table = 'CartRecipe'

    def __str__(self):
        return 'Рецепт: {} (для корзины)'.format(self.id)


class Cart(models.Model):           # Корзина

    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.CASCADE)
    recipe = models.ManyToManyField(CartRecipe, verbose_name='Рецепт', blank=True, related_name='related_cart')
    total_qty_recipes = models.PositiveIntegerField(verbose_name='Кол-во уникальных рецептов', default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая цена')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        db_table = 'Cart'

    def __str__(self):
        return str(self.id)

'''

