// обработка вывода префикса номера телефона на странице заказа
$(document).ready(function() {
	$('#id_phone_number_0 option:contains("Россия +7")').prop('selected', true).text($('#id_phone_number_0 option:selected').val());
	$('#id_phone_number_0').change(function(){
		$('#id_phone_number_0 option:selected').text($('#id_phone_number_0 option:selected').val());
	});
})