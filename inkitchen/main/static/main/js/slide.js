// активация jquery в слайдере и настройки сладера
$(document).ready(function(){
    $('.slider').slick({
        variableWidth:true,     // ширина слайдов исходя из содержимого
        slidesToShow:5,         // сколько слайдов показывать за раз
        slidesToScroll:1,       // сколько слайдов скролить за раз
        infinite:false,          // бесконечность прокрутки
        draggable:false,        // возможность скролить мышкой
        initialSlide:0,         // начальный слайд
        touchThreshold:10,      // усилие протягивания свайпом для переключения между слайдами
        waitForAnimate:false,   // ждать анимацию перехода между слайдами
        centerMode: false,      // помещать инициируемый слайд в центр
        responsive: [
            {
                breakpoint: 768,
                settings: {
                    arrows: false,
                    centerMode: true,
                    centerPadding: '40px',
                    slidesToShow: 3
                }
            },
            {
                breakpoint: 615,
                settings: {
                    arrows: false,
                    centerMode: true,
                    centerPadding: '40px',
                    slidesToShow: 1
                }
            }
        ]
    });
});