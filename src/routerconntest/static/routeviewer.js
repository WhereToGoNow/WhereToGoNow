/*
 * Class for displaying the generated routes.
 * It shows the routes using the panels.
 */

class RouteViewer {
    constructor(routeContainerId, mapContainerId, spotContainerId, submitButtonId, evaluteButtonId, onClick) {
        this.routeContainer = $(routeContainerId);
        this.mapContainer = $(mapContainerId);
        this.spotContainer = $(spotContainerId);
        this.submitButton = $(submitButtonId);
        this.evaluteButton = $(evaluteButtonId);

        this.routes = [];

        this.routeContainer.hide();
        this.spotContainer.hide();
        this.evaluteButton.hide();

        if (typeof onClick === 'undefined') {
            this.onClick = (route) => {};
        } else {
            this.onClick = onClick;
        }

        this.routeContainer.on('click', '#route', (event) => {
            // note: (event) => { ... .index(event.currentTarget) ...}
            // is equivalent to function() { ... .index(this) ...}
            var index = $('div.card').index(event.currentTarget);
            var route = this.routes[index];

            console.log(index + 'th route is selected');

            // hide the panels and show the map
            this.routeContainer.empty();
            this.routeContainer.hide();
            this.spotContainer.hide();

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
            var routeCard = $('<div>').attr('class', 'card').attr('id', 'route');
            var routeListGroup = $('<ul>').attr('id', 'list-group-route').attr('class', 'list-group list-group-flush');

            route.forEach((spot) => {
                routeListGroup.append($('<li>').attr('class', 'list-group-item').text(spot.name));
            });

            routeCard.append(routeListGroup);
            this.routeContainer.append(routeCard);
        });

        // hide the map and show the panels
        this.mapContainer.hide();
        this.spotContainer.hide();
        this.evaluteButton.show();

        this.routeContainer.show();
    }

    updateEvaluater(lastDrawnRoute, hashtags) {
        var route = lastDrawnRoute;
        var spotContainer = this.spotContainer;

        spotContainer.empty();

        if (!route) {
            console.error('route: undefined');
            return;
        }

        var spotAccordion = $('<div>').attr('id', 'accordion').attr('role', 'tablist').attr('aria-multiselectable', 'true');

        var index = 0;
        route.forEach((spot) => {

            var spotCard = $('<div>').attr('class', 'card').attr('id', 'spot');
            spotCard.append($('<div>').attr('class', 'card-header').attr('role', 'tab')
                .append($('<a>').attr('data-toggle', 'collapse').attr('data-parent', '#accordion').attr('href', '#collapse' + index).text(spot.name)));

            var collapse = $('<div>').attr('id', 'collapse' + index).attr('class', 'collapse').attr('role', 'tabpanel');
            var card_block = $('<div>').attr('class', 'card-block');

            hashtags.forEach((hashtag) => {
                card_block.append($('<button>').attr('type', 'submit').attr('class', 'btn btn-outline-primary btn-sm').text(hashtag));
            });

            collapse.append(card_block);
            spotCard.append(collapse);

            spotAccordion.append(spotCard);
            index += 1;
        });

        this.spotContainer.append(spotAccordion);

        this.mapContainer.hide();
        this.routeContainer.hide();
        this.spotContainer.show();
    }
}