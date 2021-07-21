// обработка доступности чекбокса "оставить у дверей" при нажатой radio button "Оплата онлайн"

$(document).ready(function() {
    $('input[name="pay_method"]').click(function(){
        if ($('#id_pay_method_1').is(':checked')){
            $('#id_at_door').prop('disabled', false);
        } else {
            $('#id_at_door').prop('disabled', true);
            $('#id_at_door').prop('checked', false);
        }
    })
});