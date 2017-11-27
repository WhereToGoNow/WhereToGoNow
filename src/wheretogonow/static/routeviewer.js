/*
 * Class for displaying the generated routes.
 * It shows the routes using the panels.
 */
class RouteViewer {
    constructor(args) {
        this.renderer = renderer;
        this.routeContainer = $(args.routeContainer);
        this.mapContainer = $(args.mapContainer);
        this.spotContainer = $(args.spotContainer);
        this.submitButton = $(args.submitButton);
        this.evaluateButton = $(args.evaluateButton);

        this.routes = [];

        this.routeContainer.hide();
        this.spotContainer.hide();
        this.evaluateButton.attr('disabled', true);

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

            // render the route on the map
            this.renderer.renderRoute(route);
        });

        // bind the callbacks to the buttons
        var loadingPanel = $('#panel-loading');

        this.submitButton.click(() => {
            if (this.renderer.currentStartMarker
                    && this.renderer.currentEndMarker) {
                console.log('Valid start / end markers!');
                loadingPanel.show();

                $.ajax({
                    type: 'POST',
                    url: '/update',
                    data: JSON.stringify({
                        'start': {
                            'lat': this.renderer.currentStartMarker.getPosition().lat(),
                            'lng': this.renderer.currentStartMarker.getPosition().lng()
                        },
                        'end': {
                            'lat': this.renderer.currentEndMarker.getPosition().lat(),
                            'lng': this.renderer.currentEndMarker.getPosition().lng()
                        }
                    }),
                    success: (data) => {
                        this.updateRoutes(data);
                        loadingPanel.hide();
                    },
                    error: () => {
                        loadingPanel.hide();
                    },
                    contentType: 'application/json',
                    dataType: 'json'
                });
            } else {
                alert('Missing start / end!');

                console.error(
                    'Invalid start / end markers! ('
                    + this.renderer.currentStartMarker
                    + ', '
                    + this.renderer.currentEndMarker
                    + ')'
                );
            }
        });

        this.evaluateButton.click(() => {
            $.getJSON({
                url: '/hashtags',
                success: (data) => {
                    this.updateEvaluater(
                        data,
                        signmanager.currId
                    );
                }
            });
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
            var routeListGroup = $('<ul>').attr('id', 'list-group-route')
                .attr('class', 'list-group list-group-flush');

            route.forEach((spot) => {
                var spotIcon = $('<img>').attr('src', spot.icon).css({
                    'height': '2em',
                    'margin-right': '5px',
                    'border-radius': '50%',
                    'border': '2px solid black'
                });

                var spotName = spot.name;

                // TODO: Change icon to photo
                routeListGroup.append(
                    $('<li>').attr('class', 'list-group-item')
                        .append(spotIcon)
                        .append(spotName)
                );
            });

            routeCard.append(routeListGroup);
            this.routeContainer.append(routeCard);
        });

        // hide the map and show the panels
        this.mapContainer.hide();
        this.spotContainer.hide();
        this.evaluateButton.attr('disabled', false);

        this.routeContainer.show();
    }

    updateEvaluater(hashtags, userId) {
        var route = this.renderer.lastDrawnRoute;
        var spotContainer = this.spotContainer;

        spotContainer.empty();

        console.log('update: ', this.renderer.lastDrawnRoute);
        console.log(hashtags);

        if (!route) {
            console.error('route: undefined');
            return;
        }

        var spotAccordion = $('<div>').attr('id', 'accordion')
            .attr('role', 'tablist').attr('aria-multiselectable', 'true');

        var index = 0;

        route.forEach((spot) => {
            var spotCard = $('<div>').attr('class', 'card').attr('id', 'spot');

            spotCard.append(
                $('<div>').attr('class', 'card-header')
                    .attr('role', 'tab')
                    .append($('<a>')
                    .attr('data-toggle', 'collapse')
                    .attr('data-parent', '#accordion')
                    .attr('href', '#collapse' + index).text(spot.name))
            );

            var collapse = $('<div>').attr('id', 'collapse' + index)
                .attr('class', 'collapse').attr('role', 'tabpanel');

            var card_block = $('<div>').attr('class', 'card-block');

            hashtags.forEach((hashtag) => {
                var button = $('<button>').attr('type', 'submit')
                    .attr('class', 'btn btn-outline-primary btn-sm')
                    .attr('data-spot-id', spot.id)
                    .attr('data-hashtag-id', hashtag.id)
                    .text(hashtag.name);

                button.click(() => {
                    var updateType;

                    if (button.attr('class') == 'btn btn-outline-primary btn-sm') {
                        button.attr('class', 'btn btn-primary btn-sm');
                        updateType = 'update';
                    } else {
                        button.attr('class', 'btn btn-outline-primary btn-sm');
                        updateType = 'remove';
                    }

                    $.ajax({
                        type: 'POST',
                        url: '/hashtags/update',
                        data: {
                            'userId': userId,
                            'spotId': button.attr('data-spot-id'),
                            'hashtagId': button.attr('data-hashtag-id'),
                            'updateType': updateType
                        },
                        dataType: 'json',
                        complete: (data) => {
                            console.log(data);
                        }
                    })
                });
                card_block.append(button);
            });

            collapse.append(card_block);
            spotCard.append(collapse);

            spotAccordion.append(spotCard);
            index += 1;
        });

        this.spotContainer.append(spotAccordion);

        this.evaluateButton.attr('disabled', true);
        this.mapContainer.hide();
        this.routeContainer.hide();
        this.spotContainer.show();

        $.getJSON({
            url: '/hashtags/' + userId,
            success: (evalList) => {
                console.log(evalList);

                spotAccordion.find('button').each((index, e) => {
                    var elem = $(e);

                    evalList.forEach((ev) => {
                        if (ev.userId == userId
                                && ev.spotId == elem.attr('data-spot-id')
                                && ev.hashtagId == elem.attr('data-hashtag-id')) {
                            elem.attr('class', 'btn btn-primary btn-sm');
                        }
                    });
                })
            }
        });
    }
}
