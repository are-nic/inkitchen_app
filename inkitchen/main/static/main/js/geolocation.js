// определение местоположения пользователя. Передача широты и долготы в представление и возврат адреса.
function geoFindMe(event) {
    event.preventDefault();
	const status = document.querySelector('#status');

	function success(position) {
		const latitude  = position.coords.latitude;
		const longitude = position.coords.longitude;

        $.ajax({
            data: {lat: latitude, lon: longitude},
            url: 'get_current_location',

            success: function(response) {
                status.textContent = '';
		        $("#id_address").attr("value", `${response.city} ${response.municipality} ${response.state}
		                                        ${response.street} ${response.house}`)
            },

            error: function (response) {
                console.log(response.responseJSON.errors)
            }
        });
        return false;

		//status.textContent = '';
		//mapLink.href = `https://www.openstreetmap.org/#map=18/${latitude}/${longitude}`;
		//mapLink.textContent = `Latitude: ${latitude} °, Longitude: ${longitude} °`;
	}

	function error() {
		status.textContent = 'Невозможно установить Ваше местоположение';
	}

	if(!navigator.geolocation) {
		status.textContent = 'Геолокация не поддерживается Вашим браузером';
	} else {
		status.textContent = 'Поиск…';
		navigator.geolocation.getCurrentPosition(success, error);
	}
}

document.querySelector('#find-me').addEventListener('click', geoFindMe);