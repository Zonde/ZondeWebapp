var map;
var bounds;
var markerCluster;
var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
var labelIndex = 0;

var app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        map_mac_filter: '',
        markers: [],
        bounds: null,
        ssids: [],
        ssid_label_map: null,
    },
    methods: {
        macFilter: function() {
            this.ssids = [];
            var url = 'api/'+ this.map_mac_filter +'/networks/';
            this.$http.get('api/'+ this.map_mac_filter +'/ssids/').then(response => {
                response.body.forEach(function(ssid) {
                    app.ssids.push(ssid);
                });
            });
            console.log(url)
            this.loadMap(url);
        },
        nameFilter: function(name) {
            var url = 'api/name/'+ name +'/networks/';
            this.loadMap(url);
        },
        loadMap: function(url) {
            this.markers.forEach(function(marker) { marker.setMap(null); })
            this.markers = [];

            if (markerCluster != null) {
                markerCluster.clearMarkers();
            }

            this.ssid_label_map = new Map(),
            labelIndex = 0;

            this.$http.get(url).then(response => {
                this.bounds = new google.maps.LatLngBounds();
                console.log(response);
                response.body.forEach(function(network) {
                    processMarker(network);
                });
                map.fitBounds(this.bounds);
                markerCluster = new MarkerClusterer(map, this.markers,
                        {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});

            });

        }
    },
    mounted: function() {
        this.loadMap('api/networks/')
    }
});

function processMarker(marker) {
    var position = new google.maps.LatLng(marker.latitude, marker.longitude);

    var contentString = "<h5>" + marker.ssid + "</h5>";

    var infowindow = new google.maps.InfoWindow({
        content: contentString
    });

    if (!app.ssid_label_map.has(marker.ssid)) {
        app.ssid_label_map.set(marker.ssid, labels[labelIndex]);
        labelIndex++;
    }

    var label = app.ssid_label_map.get(marker.ssid);

    var marker = new google.maps.Marker({
        position: position,
        map: map,
        animation: google.maps.Animation.DROP,
        title: marker.ssid,
        label: label,
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
