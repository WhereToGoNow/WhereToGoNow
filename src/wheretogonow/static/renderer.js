/*
 * Class for rendering the map & the routes.
 * Load this module *after* loading Google Maps API.
 */

class Renderer {
    constructor(args) {
        this.mapContainer = $(args.mapContainer);
        this.startFlagUrl = args.startFlagUrl;
        this.endFlagUrl = args.endFlagUrl;

        this.map = new google.maps.Map(this.mapContainer[0], {
            center: {
                lat: 41.89193,
                lng: 12.51133
            },
            zoom: 14
        });

        this.service = new google.maps.DirectionsService();

        this.display = new google.maps.DirectionsRenderer({
            map: this.map,
            suppressMarkers: true,
            draggable: false
        });

        this.lastDrawnRoute = null;
        this.currentInfoWindow = null;
        this.currentStartMarker = null;
        this.currentEndMarker = null;
        this.spotMarkers = [];

        // draw the markers on the map at start
        $.getJSON({
            url: '/spots',
            success: (spotList) => {
                this.renderMarkers(spotList);
            }
        });
    }

    /* Render the markers on the map. */
    renderMarkers(spotList) {
        spotList.forEach((spot) => {
            var marker = new google.maps.Marker({
                position: {
                    lat: spot.latitude,
                    lng: spot.longitude
                },
                map: this.map,
                tag: spot
            });

            var infoWindow = new google.maps.InfoWindow({
                content: spot.name
            });

            marker.addListener('click', () => {
                if (this.currentInfoWindow) {
                    this.currentInfoWindow.close();
                }

                this.currentInfoWindow = infoWindow;
                infoWindow.open(this.map, marker);
            });

            this.spotMarkers.push(marker);
        })

        this.map.addListener('click', (event) => {
            var infoWindow = new google.maps.InfoWindow({
                content: `
                    <button type="submit" id="button-start"
                            class="btn btn-info btn-sm"
                            data-lat="` + event.latLng.lat() + `"
                            data-lng="` + event.latLng.lng() + `">
                        Start
                    </button>
                    <button type="submit" id="button-end"
                        class="btn btn-success btn-sm"
                        data-lat="` + event.latLng.lat() + `"
                        data-lng="` + event.latLng.lng() + `">
                    End
                    </button>
                </div>`
            });

            infoWindow.setPosition({
                lat: event.latLng.lat(),
                lng: event.latLng.lng()
            });

            if (this.currentInfoWindow) {
                this.currentInfoWindow.close();
            }

            this.currentInfoWindow = infoWindow;
            infoWindow.open(this.map);

            google.maps.event.addListener(infoWindow, 'domready', () => {
                var infoDom = $('.gm-style-iw');

                infoDom.find('#button-start').each((index, e) => {
                    $(e).click(() => {
                        var lat = $(e).attr('data-lat') * 1;
                        var lng = $(e).attr('data-lng') * 1;
                        console.log(lat, lng);
                        console.log($(e));

                        var marker = new google.maps.Marker({
                            position: {
                                lat: lat,
                                lng: lng
                            },
                            icon: {
                                url: this.startFlagUrl,
                                scaledSize: new google.maps.Size(45, 52)
                            },
                            map: this.map
                        });

                        if (this.currentStartMarker) {
                            this.currentStartMarker.setMap(null);
                        }

                        this.currentStartMarker = marker;

                        console.log('Start: ' + marker.getPosition().lat()
                            + ', ' + marker.getPosition().lng());
                    });
                });

                infoDom.find('#button-end').each((index, e) => {
                    $(e).click(() => {
                        var lat = $(e).attr('data-lat') * 1;
                        var lng = $(e).attr('data-lng') * 1;
                        console.log(lat, lng);
                        console.log($(e));

                        var marker = new google.maps.Marker({
                            position: {
                                lat: lat,
                                lng: lng
                            },
                            icon: {
                                url: this.endFlagUrl,
                                scaledSize: new google.maps.Size(45, 52)
                            },
                            map: this.map
                        });

                        if (this.currentEndMarker) {
                            this.currentEndMarker.setMap(null);
                        }

                        this.currentEndMarker = marker;

                        console.log('End: ' + marker.getPosition().lat()
                            + ', ' + marker.getPosition().lng());
                    });
                });
            })

            this.currentInfoWindow = infoWindow;
        })
    }


    /* Given the data of a route, render the route on the map. */
    renderRoute(route) {
        var startPos = this.currentStartMarker.getPosition();
        var endPos = this.currentEndMarker.getPosition();
        var waypoints = [];

        this.clearMarkers();

        route.forEach((spot) => {
            waypoints.push({
                location: '' + spot.lat + ',' + spot.lng,
                stopover: true
            });

            var marker = new google.maps.Marker({
                position: {
                    lat: spot.lat,
                    lng: spot.lng
                },
                icon: {
                    // TODO: Change icon to photo
                    url: spot.icon,
                    scaledSize: new google.maps.Size(40, 40)
                },
                map: this.map
            });

            var infoWindow = new google.maps.InfoWindow({
                content: spot.name
            });

            marker.addListener('click', () => {
                if (this.currentInfoWindow) {
                    this.currentInfoWindow.close();
                }

                this.currentInfoWindow = infoWindow;
                infoWindow.open(this.map, marker);
            });

            this.spotMarkers.push(marker);
        });

        var routeInfo = {
            origin: '' + startPos.lat() + ',' + startPos.lng(),
            destination: '' + endPos.lat() + ',' + endPos.lng(),
            waypoints: waypoints,
            travelMode: 'WALKING',
            unitSystem: google.maps.UnitSystem.METRIC
        };

        this.service.route(routeInfo, (response, status) => {
            if (status === 'OK') {
                this.display.setDirections(response);
                console.log('Rendering: success!')
            } else {
                console.log('Rendering: failed!');
            }
        });

        this.lastDrawnRoute = route;
    }

    clearMarkers() {
        // this.currentStartMarker.setMap(null);
        // this.currentEndMarker.setMap(null);

        this.spotMarkers.forEach((marker) => {
            marker.setMap(null);
        });

        this.spotMarkers = [];
    }
}
