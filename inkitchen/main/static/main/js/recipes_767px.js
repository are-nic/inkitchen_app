// скрипт для страницы рецептов при размерах экрана от 767px и ниже
// создается два вылетающих окна - снизу корзина, сверху - дни заказа.

$(document).ready(function() {
    $(window).on('load resize', function(){
        if ($(window).width() < 768){                               // если размеры экрана меньше чем 768px

            $('#cartModal').append($('#cart_recipes_page_wrap'));   // переносим блок корзины в модальное окно
            $('#cart_lower').removeAttr('hidden');                  // удаляем атрубут скрытности блока. появляется мобильная корзина
            $('button.cartLinkModal').click(function(event){
                event.preventDefault();
                $('#cartOverlay').fadeIn(297, function(){
                    $('#cartModal')
                    .css('display', 'block')
                    .animate({opacity: 1}, 198);
                });
            });

            $('#cartModal__close, #cartOverlay').click(function(){
                $('#cartModal').animate({opacity: 0}, 198, function(){
                    $(this).css('display', 'none');
                    $('#cartOverlay').fadeOut(297);
                });
            });
        }
    });
});