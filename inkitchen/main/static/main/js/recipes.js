// обработка добавления, удаления и изменения кол-ва рецептов в корзине

$(document).ready(function(){   // после загрузки DOM-дерева (всего документа html)

    function getWeekday(){
        // функция определяет по url на какой странице дня недели заказа находится пользователь
        var url = window.location.href;
        parts = url.split("/");
        day = parts[parts.length-1];
        return day;
    };

    function btnContinue(){
        // определяем соответствует ли плану-меню кол-во блюд, добавленных в корзину.
        // меняет цвет кол-ва добавленных блюд, сообщение корзины и доступность кнопки "Далее"
        var week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
        var counter = 0;                                                                // счетчик выполнения условий заказа по каждому дню
        var all_current_meals = 0;                                                      // переменная для подсчета добавленных в корзину блюд
        var all_need_meals = $('#hidden_recipe_count').val();                           // кол-во блюд, которое нужно добавить в корзину
        week.forEach(function(weekday) {
            var current_meals = Number.parseInt($('#meals_for_' + weekday).text());     // добавленные блюда
            all_current_meals += current_meals;                                         // подсчет общего добавленного кол-ва блюд
            var need_meals = Number.parseInt($('#meals_need_for_' + weekday).text());   // кол-во блюд по плану
            if(current_meals == need_meals && all_need_meals != 0){                     // если они равны и меню не "нулевое"
                counter++;                                                              // увеличиваем счетчик дней на +1
            };
        });
        if(counter == 7){                                                               // если условие выполнилось для всех 7 дней заказа
            $('.disable-btn-next-order').attr("class", "active-btn-next-order"),        // активируем кнопку "Далее"
            $('.meals_added').css('color', 'blue'),
            $('.cart_messages').text('Все блюда добавлены!')
        }else{
            if($('.active-btn-next-order').length){                                     // если кнопка активна при неполном заказе
                $('.active-btn-next-order').attr("class", "disable-btn-next-order");    // сделать ее неактивной
                $('.meals_added').css('color', '#FC453B');                              // поменять цвет кол-ва добавленых блюд
            };
            if(all_current_meals > all_need_meals){                                     // если кол-во добавленных в корзину блюд больше необходимого
                $('.cart_messages').text('Уберите лишние блюда из корзины')             // поменять сообщение корзины
            }else if(all_current_meals < all_need_meals){                               // если кол-во добавленных в корзину блюд меньше необходимого
                $('.cart_messages').text('Добавьте блюда в корзину')
            };
        };
        counter = 0;                                                                    // обнуляем счетчик
    };

    $(".btn-add-recipe").click(function(event){         // обработка события по клику на кнопку "+" - добавления блюда в корзину
        event.preventDefault();                         // для того, чтобы страница не перезагружалась при нажатии на кнопку "+"
        var data = {};                                  // данные для отправки на сервер

        var csrf_token = $('.form_recipe_add [name="csrfmiddlewaretoken"]').val();  // присваеваем переменной csrf токен
        //data["csrfmiddlewaretoken"] = csrf_token;       // записываем токен в данные для отправки на сервер

        var id = $(this).attr("data-recipe");           // получаем id рецепта, который добавляем в корзину сессии
        data.recipe_id = id;                            // записываем id в данные для отправки на сервер

        var delivery_date = $(this).attr("data-date");  // получаем дату доставки
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
                if(!$('#recipe_id_' + id).length) {     // если в корзине нет блюда с таким id
                    $("#cart_recipes_block").append(    // добавляем блюдо в корзину
                        '<div class="cart-item" id="recipe_id_' + id +'">' +
                            '<div class="aside">' +
                                '<img src="' + meal_image + '"' + 'class="img-sm">' +
                            '</div>' +
                            '<div class="info">' +
                                '<div class="info-title">' +
                                    '<a href="" class="title text-dark" data-abc="true">'+ meal_name + '</a>'+
                                    '<button type="submit" class="btn-del_from_cart" data-recipe="' + id + '" data-date="' + delivery_date + '">x</button>'+
                                '</div>'+
                                '<div class="meal_count_cart">'+
                                    '<button type="button" onclick="this.nextElementSibling.stepDown()" class="minus" data-recipe="' + id + '" data-date="' + delivery_date + '">-</button>'+
                                    '<input class="q_portion" type="number" min="1" max="99" value="'+ meal_qty +'" readonly">'+
                                    '<button type="button" onclick="this.previousElementSibling.stepUp()" class="plus" data-recipe="' + id + '" data-date="' + delivery_date + '">+</button>'+
                                '</div>'+
                            '</div>'+
                        '</div>'),
                    // при добавлении блюда в корзину, находим в списке дней и в корзине текущее кол-во добавленных блюд
                    // превращаем строку в число и увеличиваем их на 1, подставляя новое значение вместо старого
                    day = getWeekday()
                    // находим текущее кол-во добавленных блюд в дне заказа в блоке недели и превращаем в число
                    var cur_qty_meals = Number.parseInt($('#meals_for_' + day).text());
                    $('#meals_for_' + day).text(cur_qty_meals + 1); // прибавляем +1 к кол-ву добавленных блюд
                    // обновленное кол-во подставляем вместо текущего кол-ва добавленных блюд в корзине
                    $(".meals_added").text($('#meals_for_' + day).text());

                    btnContinue();
                }else{
                    meal_qty++;
                    $('#recipe_id_' + id).find('.q_portion').attr('value', meal_qty);
                };
            },

            error: function(){                           // при ошибке с сервера
                alert('Error recipe add!');              // вылетает алерт-окно об ошибке в этом разделе
            },
        });
    });

    // добавление кол-ва порций внутри корзины
    $(document).on("click", "button.plus", function(event){
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
            url: '../../cart/adjust',                   // url для отправки данных в adjust_cart
            data: data,
            success: function(response){
                console.log('more meals...')
            },
            error: function(){
                alert('Error quantity plus!');
            },
        })
    });

    // уменьшение кол-ва порций внутри корзины
    $(document).on("click", "button.minus", function(event){
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
            url: '../../cart/adjust',                   // url для отправки данных в adjust_cart
            data: data,
            success: function(response){
                console.log('less meals...')
            },
            error: function(){
                alert('Error quantity minus!');
            },
        })
    });

    // удаление рецепта из корзины при нажатии на "х" (сначала загружаем документ заново, т.к. появились новые элементы на странице)
    $(document).on("click", ".btn-del_from_cart", function(event){
        event.preventDefault();
        var data = {};

        var id = $(this).attr("data-recipe");           // получаем id рецепта, который следует удалить
        data.recipe_id = id;                            // заносим его в словарь данных для отправки на сервер
        var delivery_date = $(this).attr("data-date");  // получаем дату доставки
        data.delivery_date = delivery_date;             // заносим ее в словарь данных для отправки на сервер

        $.ajax({
            url: '../../cart/remove',                   // url для отправки данных в remove_from_cart
            data: data,
            success: function(response){
                console.log('recipe was removing')
                $("#recipe_id_" + id).remove();         // удалить рецепт из корзины (DOM-дерева)

                day = getWeekday()
                // уменьшение кол-ва добавленных блюд в блоке дней недели и корзине
                var cur_qty_meals = Number.parseInt($('#meals_for_' + day).text());
                $('#meals_for_' + day).text(cur_qty_meals - 1);
                // обновленное кол-во подставляем вместо текущего кол-ва добавленных блюд в корзине
                $(".meals_added").text($('#meals_for_' + day).text());

                btnContinue();
            },
            error: function(){
                alert('Error remove recipe!');
            },
        })
    });

    // задаем стили выделения кнопки дня недели в соответсвии с открытой страницей дня недели
    day = getWeekday();
    button_day = $("#" + day).css({'background': '#e5433a', 'color': 'white'});

    btnContinue();
})