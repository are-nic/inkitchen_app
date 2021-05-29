// проверка на валидность емайл при регистрации

$(document).ready(function () {
    // поймать событие отправки формы
    $('#register_email').keyup(function () {
        // создаем вызов AJAX
        $.ajax({
             data: $(this).serialize(), // получить данные из формы
             url: 'users/validate_email',
             // При успешном вызове
             success: function (response) {
                  if (response.is_taken == true) {
                       $('#register_email').removeClass('is-valid').addClass('is-invalid');
                       $('.registerLinkModal').after('<div class="invalid-feedback d-block" id="emailError">Этот Email уже занят</div>')
                  } else {
                       $('#register_email').removeClass('is-invalid').addClass('is-valid');
                       $('#emailError').remove();
                  }
             },
             // При ошибке
             error: function (response) {
                // предупреждение об ошибке в консоли
                console.log(response.responseJSON.errors)
             }
        });
        return false;   // предотвращает отправку формы, тем самым предотвращая перезагрузку страницы
    });
})