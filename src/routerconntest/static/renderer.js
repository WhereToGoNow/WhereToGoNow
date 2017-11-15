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
                lat: 36.369392,
                lng: 127.364025
            },
            zoom: 7
        });

        // attach the renderer
        this.display.setMap(this.map);
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