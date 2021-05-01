// обработка добавления рецептов в корзину
$(document).ready(function(){                           // общая обертка для выполнения скрипта после загрузки всего документа html
    $(".btn-add-recipe").click(function(event){         // обработка события по клику на кнопку "+" - добавления блюда в корзину
        event.preventDefault();                         // для того, чтобы страница не перезагружалась при нажатии на кнопку "+"
        var data = {};                                  // данные для отправки на сервер

        var csrf_token = $('.form_recipe_add [name="csrfmiddlewaretoken"]').val();  // присваеваем переменной csrf токен
        //data["csrfmiddlewaretoken"] = csrf_token;       // записываем токен в данные для отправки на сервер

        var id = $(this).attr("data-recipe");           // получаем id рецепта, который добавляем в корзину сессии
        data.recipe_id = id;                            // записываем id в данные для отправки на сервер

        var meal_name = $(this).data("name");           // присваеваем переменной заголовок рецепта
        var meal_image = $(this).data("image");         // присваеваем переменной url фото рецепта

        var meal_qty;                                   // кол-во порций при нажатии на добавление блюда в корзину
        if(!$('#recipe_id_' + id).length) {             // если на странице нет элемента с таким id (блюда нет в корзине)
            meal_qty = 1;                               // кол-во порций = 1
        }else{
           meal_qty = $('#recipe_id_' + id).find('.raz').val(); // кол-во порций = значению уже добавленного кол-ва в корзину
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
                                    '<form action="{% url ' + "'remove_from_cart'" + id + ' %}">'+
                                        '<button type="submit" class="btn btn-sm">x</button>'+
                                    '</form>'+
                                '</div>'+
                                '<div class="meal_count_cart">'+
                                    '<button type="button" onclick="this.nextElementSibling.stepDown()" class="minus">-</button>'+
                                    '<input type="number" min="0" max="100" value="'+ meal_qty +'" readonly class="raz">'+
                                    '<button type="button" onclick="this.previousElementSibling.stepUp()" class="plus">+</button>'+
                                '</div>'+
                            '</div>'+
                        '</div>')
                }else{
                    meal_qty++;
                    $('#recipe_id_' + id).find('.raz').attr('value', meal_qty);
                }
            },

            error: function(){                           // при ошибке с сервера
                alert('Error!');
            },
        })
    });
})