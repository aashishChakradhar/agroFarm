document.addEventListener('DOMContentLoaded', () => {
    const lat = document.querySelector('.locationpoint').getAttribute('data-lat');
    const long = document.querySelector('.locationpoint').getAttribute('data-long');

    navigator.geolocation.getCurrentPosition(showPosition, error, options);
    function showPosition(position){
        let endLati = position.coords.latitude;
        let endLongi = position.coords.longitude;

        console.log(endLati)
        console.log(endLongi)
    }	

    function error(err) {
        console.warn(`ERROR(${err.code}): ${err.message}`);
    }

    var options = {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0
    };
})