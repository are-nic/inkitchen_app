from ...models import TagIngredient, Product, Shop
from django.core.management.base import BaseCommand
import requests


def get_products():
    """
    Получение продуктов магазинов по id тега ингредиента
    Заносит в БД данные по магазинам и продуктам
    """
    # получаем данные по конкретному тегу ингредиента
    # (название продукта, его цена, остатки на складах магазинов, наименование магазина)

    # проходим по всем тегам в БД и укаываем в качестве параметра id каждого тега
    for tag in TagIngredient.objects.all():
        data = requests.get(
            'https://api.kitchenhub.club/v1/export-recept/export-tovar-by-tag-id',
            params={'id': tag.id}
        )
        print(tag.id)
        if data.status_code == 200:
            # переводим данные запроса в JSON
            data_shops = data.json()
            # проходим циклом по всем id магазинов, продающих данный ингредиент
            for shop_id in data_shops["data"]:
                # проходим по списку продуктов конркетного магазина
                for product in data_shops['data'][shop_id]['1']:
                    # если в БД нет записи об этом магазине
                    if not Shop.objects.filter(id=product['shop']['id']).exists():
                        shop = Shop(
                            id=product['shop']['id'],
                            name=product['shop']['nameForm'],
                            logo=product['shop']['logoForm']
                        )
                        shop.save()

                    product_db = Product(
                        id=product['id'],
                        shop=Shop.objects.get(id=product['shop']['id']),
                        name=product['name'],
                        qty_per_item=product['valuecount'],
                        stock=product['countstore'],
                        price=product['pricepercount'],
                        unit=product['value']['name'],
                        tag=TagIngredient.objects.get(id=tag.id),
                    )
                    product_db.save()
            # удаление тега ингредиента из БД при условии отсутствия товаров по этому тегу
            if Product.objects.filter(tag=tag.id).count() == 0:
                tag.delete()

        else:
            print(data.status_code, 'не удалось выполнить запрос к по тегу {}'.format(tag.name))
    print('complete')
    return


def clear_data():
    """
    Очистить все записи в таблице Product
    """
    Product.objects.all().delete()


class Command(BaseCommand):
    def handle(self, *args, **options):
        clear_data()
        get_products()
        print("Данные магазинов и продуктов занесены в БД")

"""
каждый product в списке products имеет следующий вид на примере одного экземпляра
{
    'id': 14, 
    'user_id': 5, 
    'name': 'Картофель белый мытый', 
    'valuecount': 100, 
    'countstore': 999, 
    'price': None, 
    'pricepercount': '30.00', 
    'shopidproduct': '1017', 
    'minvaluecount': 1, 
    'valuecountOriginal': '100.000', 
    'brands_id': 9, 
    'brand': {
        'id': 9, 
        'name': '', 
        'isNew': 0
        }, 
    'values_id': 1, 
    'value': {
        'id': 1, 
        'name': 'гр.', 
        'description': 'Граммы', 
        'isNew': 1
        }, 
    'tags': [
        {
            'id': 371, 
            'name': 'картофель', 
            'slug': 'kartofel', 
            'isNew': 0, 
            'unactual': 0
        }
    ], 
    'shop': {
        'id': 5, 
        'username': 'dorogomil', 
        'logoForm': 'https://dorogomilovo24.ru/image/catalog/logo1.png', 
        'nameForm': 'Дорогомиловский', 
        'actionurl': 'https://dorogomilovo24.ru/index.php?route=checkout/cart/addtocart', 
        'url': 'https://dorogomilovo24.ru'
        }, 
    'isNew': 0, 
    'isGood': 1
}
"""