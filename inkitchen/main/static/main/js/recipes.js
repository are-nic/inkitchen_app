// обработка добавления, удаления рецептов и изменения их кол-ва в корзине

// общая обертка для выполнения скрипта после загрузки всего документа html
$(document).ready(function(){
    // функция определяет по url на какой странице дня недели заказа находится пользователь
    function getWeekday(){
        var url = window.location.href;
        parts = url.split("/");
        day = parts[parts.length-1];
        return day;
    };

    $(".btn-add-recipe").click(function(event){         // обработка события по клику на кнопку "+" - добавления блюда в корзину
        event.preventDefault();                         // для того, чтобы страница не перезагружалась при нажатии на кнопку "+"
        var data = {};                                  // данные для отправки на сервер

        var csrf_token = $('.form_recipe_add [name="csrfmiddlewaretoken"]').val();  // присваеваем переменной csrf токен
        //data["csrfmiddlewaretoken"] = csrf_token;       // записываем токен в данные для отправки на сервер

        var id = $(this).attr("data-recipe");           // получаем id рецепта, который добавляем в корзину сессии
        data.recipe_id = id;                            // записываем id в данные для отправки на сервер

        var delivery_date = $(this).attr("data-date");   // получаем дату доставки
        data.delivery_date = delivery_date;             // записываем дату доставки в данные для отправки на сервер

        var meal_name = $(this).data("name");           // присваеваем переменной заголовок рецепта
        var meal_image = $(this).data("image");         // присваеваем переменной url фото рецепта

        var meal_qty;                                   // кол-во порций при нажатии на добавление блюда в корзину
        if(!$('#recipe_id_' + id).length) {             // если на странице нет элемента с таким id (блюда нет в корзине)
            meal_qty = 1;                               // кол-во порций = 1
        }else{
           meal_qty = $('#recipe_id_' + id).find('.q_portion').val(); // кол-во порций = значению уже добавленного кол-ва в корзину
           meal_qty = Number.parseInt(meal_qty);        // преобразовываем полученное значение в число
        };

        var url = $(".form_recipe_add").attr("action"); // url для запроса ajax (add_to_cart)
        $.ajax({
            type: "get",                                // можно не указывать, т. к. по умолчанию GET
            url: url,                                   // роут, по которому мы направим асинхронный запрос с данными на сервер
            data: data,                                 // данные для отправки на сервер
            success: function(response){                // при удачном ответе с сервера
                if(!$('#recipe_id_' + id).length) {     // если на странице нет элемента с таким id (блюда нет в корзине)
                    $("#cart_recipes_block").append(    // добавляем блюдо в корзину в виде html-кода
                        '<div class="cart-item" id="recipe_id_' + id +'">' +
                            '<div class="aside">' +
                                '<img src="' + meal_image + '"' + 'class="img-sm">' +
                            '</div>' +
                            '<div class="info">' +
                                '<div class="info-title">' +
                                    '<a href="" class="title text-dark" data-abc="true">'+ meal_name + '</a>'+
                                    '<button type="submit" class="btn-del_from_cart">x</button>'+
                                '</div>'+
                                '<div class="meal_count_cart">'+
                                    '<button type="button" onclick="this.nextElementSibling.stepDown()" class="minus">-</button>'+
                                    '<input type="number" min="0" max="100" value="'+ meal_qty +'" readonly class="q_portion">'+
                                    '<button type="button" onclick="this.previousElementSibling.stepUp()" class="plus">+</button>'+
                                '</div>'+
                            '</div>'+
                        '</div>')
                }else{
                    meal_qty++;
                    $('#recipe_id_' + id).find('.q_portion').attr('value', meal_qty);
                }

                // при добавлении блюда в корзину, находим в списке дней и в корзине текущее кол-во добавленных блюд
                // превращаем строку в число и увеличиваем их на 1, подставляя новое значение вместо старого
                day = getWeekday()
                // находим текущее кол-во добавленных блюд в дне заказа в блоке недели и превращаем в число
                var cur_qty_meals = Number.parseInt($('#meals_for_' + day).text());
                $('#meals_for_' + day).text(cur_qty_meals + 1); // прибавляем +1 к кол-ву добавленных блюд
                // обновленное кол-во подставляем вместо текущего кол-ва добавленных блюд в корзине
                $("#next_btn_wrap span").text($('#meals_for_' + day).text());
            },

            error: function(){                           // при ошибке с сервера
                alert('Error recipe add!');              // вылетает алерт-окно об ошибке в этом разделе
            },
        })
    });

    // добавление кол-ва порций внутри корзины
    $("button.plus").click(function(event){
        event.preventDefault();
        var data = {};

        var id = $(this).attr("data-recipe");           // получаем id рецепта, кол-во которого увеличиваем
        data.recipe_id = id;

        var delivery_date = $(this).attr("data-date");  // получаем дату доставки
        data.delivery_date = delivery_date;

        var quantity_plus = true;                       // переменная, обозначающая именно увеличение кол-ва
        data.quantity_plus = quantity_plus;

        var quantity = $("input.q_portion").val();      // получаем текущее кол-во порций в корзине со страницы рецептов
        data.quantity = quantity;

        $.ajax({
            url: '../../cart/adjust',                         // url для отправки данных в adjust_cart
            data: data,
            success: function(response){
                console.log('больше')
            },
            error: function(){
                alert('Error quantity plus!');
            },
        })
    });

    // уменьшение кол-ва порций внутри корзины
    $("button.minus").click(function(event){
        event.preventDefault();
        var data = {};

        var id = $(this).attr("data-recipe");           // получаем id рецепта, кол-во которого уменьшаем
        data.recipe_id = id;

        var delivery_date = $(this).attr("data-date");  // получаем дату доставки
        data.delivery_date = delivery_date;

        var quantity_minus = true;                      // переменная, обозначающая именно уменьшение кол-ва
        data.quantity_minus = quantity_minus;

        var quantity = $("input.q_portion").val();      // получаем текущее кол-во порций в корзине со страницы рецептов
        data.quantity = quantity;

        $.ajax({
            url: '../../cart/adjust',                         // url для отправки данных в adjust_cart
            data: data,
            success: function(response){
                console.log('меньше')
            },
            error: function(){
                alert('Error quantity minus!');
            },
        })
    });

    // удаление рецепта из корзины при нажатии на "х"
    $(".btn-del_from_cart").click(function(event){
        event.preventDefault();
        var data = {};

        var id = $(this).attr("data-recipe");           // получаем id рецепта, кол-во которого уменьшаем
        data.recipe_id = id;

        var delivery_date = $(this).attr("data-date");  // получаем дату доставки
        data.delivery_date = delivery_date;

        $.ajax({
            url: '../../cart/remove',                   // url для отправки данных в remove_from_cart
            data: data,
            success: function(response){
                console.log('рецепт удален')
                $("#recipe_id_" + id).remove();         // удалить рецепт из корзины (DOM-дерева)

                day = getWeekday()
                // уменьшение кол-ва добавленных блюд в блоке дней недели и корзине
                var cur_qty_meals = Number.parseInt($('#meals_for_' + day).text());
                $('#meals_for_' + day).text(cur_qty_meals - 1);
                // обновленное кол-во подставляем вместо текущего кол-ва добавленных блюд в корзине
                $("#next_btn_wrap span").text($('#meals_for_' + day).text());
            },
            error: function(){
                alert('Error remove recipe!');
            },
        })
    });

    // задаем стили выделения кнопки дня недели в соответсвии с открытой страницей дня недели
    day = getWeekday()
    button_day = $("#" + day).css({'background': '#e5433a', 'color': 'white'});
})