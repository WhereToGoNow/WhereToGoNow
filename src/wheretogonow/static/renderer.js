/*
 * Class for rendering the map & the routes.
 * Load this module *after* loading Google Maps API.
 */

class Renderer {


    constructor(mapContainerId) {
        this.lastDrawnRoute = null;
        this.lastDrawnArrowRoute = null;

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

                        console.log('Picked '
                            + marker.getPosition().lat()
                            + ', '
                            + marker.getPosition().lng()
                            + ' as start!');
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

                        console.log('Picked '
                            + marker.getPosition().lat()
                            + ', '
                            + marker.getPosition().lng()
                            + ' as end!');
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
        console.log('Rendering ' + route + ' ...');

        // var startSpot = route[0];
        // var endSpot = route[route.length - 1];
        // var middleSpots = route.slice(1, route.length - 3);
        var middleSpots = route;

        // pack the middle spots into waypoints
        var waypoints = [];

        middleSpots.forEach((spot) => {
            waypoints.push({
                location: 'place_id:' + spot.id,
                stopover: true
            });
        });

        // draw the route on the map
        var startPos = this.currentStartMarker.getPosition();
        var endPos = this.currentEndMarker.getPosition();

        var routeInfo = {
            origin: '' + startPos.lat() + ',' + startPos.lng(),
            destination: '' + endPos.lat() + ',' + endPos.lng(),
            waypoints: waypoints,
            travelMode: 'DRIVING',
            unitSystem: google.maps.UnitSystem.METRIC
        };

        // erase arrow route
        if (this.lastDrawnArrowRoute != null) {
            this.lastDrawnArrowRoute.setMap(null);
        }

        // try to draw the route / if it fails, draw the route with arrows
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

    renderArrowRoute(route) {
        var symbol = {path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW};
        var spots = [];
        var startPos = this.currentStartMarker.getPosition();
        var endPos = this.currentEndMarker.getPosition();

        spots.push({
            lat: startPos.lat(),
            lng: startPos.lng()
        });

        route.forEach((spot) => {
            spots.push({
                lat: spot.lat,
                lng: spot.lng
            });
        });

        spots.push({
            lat: endPos.lat(),
            lng: endPos.lng()
        });

        this.lastDrawnArrowRoute = new google.maps.Polyline({
            path: spots,
            icons: [{icon: symbol, offset: '100%'}],
            map: this.map
        });
    }
}