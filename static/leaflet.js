var map = L.map('map').setView([60.171019, 24.941518], 13);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var _geocoderType = L.Control.Geocoder.nominatim();

var geocoder = L.Control.geocoder({
    geocoder: _geocoderType
}).addTo(map);

geocoder.on('markgeocode', function (event) {
    var center = event.geocode.center;
    L.marker(center).addTo(map);
    map.setView(center, map.getZoom());
         $.ajax({
            url: '/newrestaurant',
            method: 'POST',
            data: JSON.stringify({ center: center}),
            contentType: 'application/json'
        });
});
