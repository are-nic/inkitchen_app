// скрипт для добавления продуктов маркета в корзину
var addBtns = document.getElementsByClassName('btn_add_product_market')

for (i = 0; i < addBtns.length; i++) {
    addBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)
    })
}