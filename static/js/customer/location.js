document.addEventListener('DOMContentLoaded', () => {
    const lat = document.querySelector('.locationpoint').getAttribute('data-lat');
    const long = document.querySelector('.locationpoint').getAttribute('data-long');

    const locations = document.querySelectorAll('.locationpoint');

    navigator.geolocation.getCurrentPosition(showPosition, error, options);

    function getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2) {
        var R = 6371;
        var dLat = deg2rad(lat2-lat1);
        var dLon = deg2rad(lon2-lon1); 
        var a = 
          Math.sin(dLat/2) * Math.sin(dLat/2) +
          Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * 
          Math.sin(dLon/2) * Math.sin(dLon/2)
          ; 
        var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
        var d = R * c;
        return d;
    }
    
    function deg2rad(deg) {
        return deg * (Math.PI/180)
    }

    function showPosition(position){
        let endLati = position.coords.latitude;
        let endLongi = position.coords.longitude;

        locations.forEach( (item) =>{
            let lat = item.getAttribute('data-lat');
            let long = item.getAttribute('data-long');

            if(getDistanceFromLatLonInKm(lat, long, endLati, endLongi) >= 5){
                item.classList.add('out-of-area');
                console.log('far');
            }
            console.log(getDistanceFromLatLonInKm(lat, long, endLati, endLongi));
        })
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