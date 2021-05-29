$(document).ready(function() {
    $(window).on('load resize', function(){
        if ($(window).width() < 768){                               // если размеры экрана меньше 768px
            $(".remove_recipe").text("x");
            $(".change_recipe").text("...");
            $("#column_change_recipe").text("Изм.");
        };
    })
});