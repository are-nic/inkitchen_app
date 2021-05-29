// вывод всплывающей карточки рецепта на странице рецептов

$(document).ready(function() {
    $('a.recipeLinkModal').click(function(event){
        event.preventDefault();
        var id = $(this).attr("data-id");
        var title = $(this).attr("data-title");
        var image = $(this).attr("data-image");
        var description = $(this).attr("data-description");
        var kkal = $(this).attr("data-kkal");
        var protein = $(this).attr("data-protein");
        var fat = $(this).attr("data-fat");
        var carbo = $(this).attr("data-carbo");
        var time = $(this).attr("data-time");
        var data = {};
        data.id = id;
        var url = '../../recipes/ingredients';

        $.ajax({
            url: url,
            data: data,
            success: function(response){
                $(".title-recipe h3").text(title);
                $(".img-recipe img").attr("src", image);
                $(".description_recipe p").text(description);
                $(".value_energy_kkal").text(kkal);
                $(".value_energy_pfc").text(protein + "/" + fat + "/" + carbo);
                $(".cook_time strong").text(time);
                // перебираем словарь ингридиентов и их значений
                for (const [ingredient, values] of Object.entries(response.ingredients)){
                    $(".ingredient_list-card").append($("<p>", {'text': ingredient +' '+ values[0] +' '+ values[1]}))
                };

                $('#recipeOverlay').fadeIn(297, function(){
                    $('#recipeModal')
                    .css('display', 'block')
                    .animate({opacity: 1}, 198);
                });

                $('#recipeModal__close, #recipeOverlay').click(function(){
                    $(".ingredient_list-card").empty();
                    $('#recipeModal').animate({opacity: 0}, 198,
                    function(){
                        $(this).css('display', 'none');
                        $('#recipeOverlay').fadeOut(297);
                    });
                });
            },
            error: function(){
                alert('Error recipe pop_up!');
            },
        });
    });
});