/*
 * Class for rendering the map & the routes.
 * Load this module *after* loading Google Maps API.
 */

class Renderer {


    constructor(mapContainerId) {
        this.lastDrawnRoute = null;

        this.mapContainer = $(mapContainerId);
        this.service = new google.maps.DirectionsService();
        this.display = new google.maps.DirectionsRenderer();

        this.map = new google.maps.Map(this.mapContainer[0], {
            center: {
                lat: 41.89193,
                lng: 12.51133
            },
            zoom: 14
        });
        // attach the renderer
        this.display.setMap(this.map);
    }

    renderMarkers($, spotList) {

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
        })

        this.map.addListener('click', (event) => {
            var infoWindow = new google.maps.InfoWindow({
                content: ` <button type="submit" id="button-start" class="btn btn-info btn-sm" data-lat="` + event.latLng.lat() + `" data-lng="` + event.latLng.lng() + `">Start</button>
                        <button type="submit" id="button-end" class="btn btn-success btn-sm" data-lat="` + event.latLng.lat() + `" data-lng="` + event.latLng.lng() + `">End</button>
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
                            label: 'start',
                            map: this.map
                        });

                        if (this.currentStartMarker) {
                            this.currentStartMarker.setMap(null);
                        }
                        this.currentStartMarker = marker;
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
                            label: 'end',
                            map: this.map
                        });

                        if (this.currentEndMarker) {
                            this.currentEndMarker.setMap(null);
                        }
                        this.currentEndMarker = marker;
                    });
                });
            })

            this.currentInfoWindow = infoWindow;
        })
    }


    /*
     * Given the data of a route, render the route on the map.
     * Format of route:
     * {
     *     (spot's name): {
     *         name: (spot's (real) name),
     *         ...
     *     },
     *     ...
     * }
     */
    renderRoute(route) {
        console.log(route);

        var startSpot = route[0];
        var endSpot = route[route.length - 1];
        var middleSpots = route.slice(1, route.length - 3);

        // pack the middle spots into waypoints
        var waypoints = [];

        middleSpots.forEach((spot) => {
            waypoints.push({
                location: spot['name'],
                stopover: true
            });
        });

        // draw the route on the map
        var routeInfo = {
            origin: startSpot['name'],
            destination: endSpot['name'],
            waypoints: waypoints,
            travelMode: 'DRIVING',
            unitSystem: google.maps.UnitSystem.METRIC
        };

        this.service.route(routeInfo, (response, status) => {
            if (status === 'OK') {
                this.display.setDirections(response);
            } else {
                // do nothing
            }
        });

        this.lastDrawnRoute = route;
    }
}