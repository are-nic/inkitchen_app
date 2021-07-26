// скрипт для добавления продуктов маркета в корзину
var addBtns = document.getElementsByClassName('btn_add_product_market')

for (i = 0; i < addBtns.length; i++) {
    addBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)
    })
}
// открытие и закрытие форм заказа под стрелками
$(document).ready(function(){
    $('.check-arrow_address, #title_address_forms').click(function(){
         $('#content_block_address').slideToggle(100, function(){
              if ($(this).is(':hidden')) {
                   $('.check-arrow_address').removeClass('open');
              } else {
                   $('.check-arrow_address').addClass('open');
              }
         });
         return false;
    });
    $('.check-arrow_pay_method, #title_pay_method_forms').click(function(){
         $('#content_block_pay_method').slideToggle(100, function(){
              if ($(this).is(':hidden')) {
                   $('.check-arrow_pay_method').removeClass('open');
              } else {
                   $('.check-arrow_pay_method').addClass('open');
              }
         });
         return false;
    });
    $('.check-arrow_promo, #title_promo_forms').click(function(){
         $('#content_block_promo').slideToggle(100, function(){
              if ($(this).is(':hidden')) {
                   $('.check-arrow_promo').removeClass('open');
              } else {
                   $('.check-arrow_promo').addClass('open');
              }
         });
         return false;
    });
});