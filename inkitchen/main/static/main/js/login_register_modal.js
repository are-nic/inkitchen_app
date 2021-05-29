// вывод модальных окон регистрации и логина на главной странице

$(document).ready(function() {
  $('.registerLinkModal').click( function(event){
    event.preventDefault();
    var email = $('.continue-register-form #register_email').val();
    $('.form-group #register_email').attr('value', email);

    $('#registerOverlay').fadeIn(297, function(){
      $('#registerModal')
      .css('display', 'block')
      .animate({opacity: 1}, 198);
    });
  });

  $('#registerModal__close, #registerOverlay').click( function(){
    $('#registerModal').animate({opacity: 0}, 198,
      function(){
        $(this).css('display', 'none');
        $('#registerOverlay').fadeOut(297);
    });
  });
});

// вывод окна логина
$(document).ready(function() {
  $('.loginLinkModal').click( function(event){
    event.preventDefault();
    $('#loginOverlay').fadeIn(297, function(){
      $('#loginModal')
      .css('display', 'block')
      .animate({opacity: 1}, 198);
    });
  });

  $('#loginModal__close, #loginOverlay').click( function(){
    $('#loginModal').animate({opacity: 0}, 198,
      function(){
        $(this).css('display', 'none');
        $('#loginOverlay').fadeOut(297);
    });
  });
});