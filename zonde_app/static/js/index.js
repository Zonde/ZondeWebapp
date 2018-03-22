var map;
var bounds;

var app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        markers: [],
        bounds: null
    },
    methods: {
        loadMap: function() {
            this.$http.get('/api/networks/').then(response => {
                this.bounds = new google.maps.LatLngBounds();
                response.body.forEach(function(network) {
                    processMarker(network);
                });
                map.fitBounds(this.bounds);
            });
        }
    },
    mounted: function() {
        this.loadMap()
    }
});

function processMarker(marker) {
    var position = new google.maps.LatLng(marker.latitude, marker.longitude);

    var contentString = "<h5>" + marker.ssid + "</h5>";

    var infowindow = new google.maps.InfoWindow({
        content: contentString
    })

    var marker = new google.maps.Marker({
        position: position,
        map: map,
        animation: google.maps.Animation.DROP,
        title: marker.ssid,
    });

    marker.addListener('click', function() {
        infowindow.open(map, marker);
    })

    app.markers.push(marker);

    app.bounds.extend(position);
}

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {});
}
