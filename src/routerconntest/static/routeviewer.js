/*
 * Class for displaying the generated routes.
 * It shows the routes using the panels.
 */

class RouteViewer {
    constructor(routeContainerId, mapContainerId, onClick) {
        this.routeContainer = $(routeContainerId);
        this.mapContainer = $(mapContainerId);
        this.routes = [];

        if (typeof onClick === 'undefined') {
            this.onClick = (route) => {};
        } else {
            this.onClick = onClick;
        }

        this.routeContainer.on('click', '#route', (event) => {
            // note: (event) => { ... .index(event.currentTarget) ...}
            // is equivalent to function() { ... .index(this) ...}
            var index = $('li.panel').index(event.currentTarget);
            var route = this.routes[index];

            console.log(index +'th route is selected');

            // hide the panels and show the map
            this.routeContainer.empty();
            this.routeContainer.hide();
            this.mapContainer.show();

            // callback (ex. render the map)
            this.onClick(route);
        });
    }

    updateRoutes(routes) {
        if (!routes) {
            console.error('routes: undefined');
            return;
        }

        this.routes = routes;

        // generate the panels
        this.routeContainer.empty();

        this.routes.forEach((route) => {
            var routePanelHeader = $('<div>').attr('class', 'panel-heading')
                .text(route[0]['name']);

            var routePanelFooter = $('<div>').attr('class', 'panel-footer')
                .text(route[route.length - 1]['name']);

            var routePanelBody = $('<div>').attr('class', 'panel-body');

            for (var i = 1; i < route.length - 1; i++) {
                routePanelBody.append(route[i]['name'] + '<br />');
            }

            var routePanel = $('<li>').attr('class', 'panel panel-primary')
                .attr('id', 'route')
                .append(routePanelHeader, routePanelBody, routePanelFooter);

            this.routeContainer.append(routePanel);
        });

        // hide the map and show the panels
        this.mapContainer.hide();
        this.routeContainer.show();
    }
}
