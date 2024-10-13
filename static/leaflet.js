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


document.addEventListener('DOMContentLoaded', function() {
    fetch('/newrestaurant')
        .then(response => response.json())
        .then(data => {
            const selectElement = document.getElementById('validatedInputGroupSelect');

            while (selectElement.firstChild) {
                selectElement.removeChild(selectElement.firstChild);
            }

            data.options.forEach(option => {
                const optionElement = document.createElement('option');
                optionElement.value = option.id;
                optionElement.textContent = option.text;
                selectElement.appendChild(optionElement);
            });

            if (selectElement.length > 1) {
                selectElement.selectedIndex = 1;
            }
        })
        .catch(error => console.error('Fetching categories failed:', error));
});
