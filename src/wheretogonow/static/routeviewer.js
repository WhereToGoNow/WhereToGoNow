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

        this.currentRoutes = [];
        this.currentSelectedRoute = null;

        this.routeContainer.hide();
        this.spotContainer.hide();
        this.disableEvaluation();

        var loadingPanel = $('#panel-loading');

        this.routeContainer.on('click', '#route', (event) => {
            // note: (event) => { ... .index(event.currentTarget) ...}
            // is equivalent to function() { ... .index(this) ...}
            var index = $('div.card').index(event.currentTarget);

            this.currentSelectedRoute = this.currentRoutes[index];
            console.log(index + 'th route is selected');

            this.enableEvaluation();
            this.openMapContainer();

            // render the route on the map
            this.renderer.renderRoute(this.currentSelectedRoute);
        });

        this.submitButton.click(() => {
            this.disableEvaluation();

            // if the user choosed both start / end markers,
            // request the route from the server
            if (this.renderer.currentStartMarker
                    && this.renderer.currentEndMarker) {
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
                        },
                        'time': this.renderer.currentTime
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
                    'Error in submitButton: Invalid start / end markers! ('
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
            console.error('Error in updateRoutes(): Invalid routes!');
            return;
        }

        // store the routes
        this.currentRoutes = routes;

        // generate the panels
        this.routeContainer.empty();

        this.currentRoutes.forEach((route) => {
            var routeCard = $('<div>').attr('class', 'card').attr('id', 'route');
            var routeListGroup = $('<ul>').attr('id', 'list-group-route')
                .attr('class', 'list-group list-group-flush');
            var spotCount = route.length;

            for (var i = 0; i < spotCount; i++) {
                var bgColor;
                var iconHeight;
                var nameSize;

                if (i === 0) {
                    bgColor = '#4EF425';
                    iconHeight = '2em';
                    nameSize = '100%';
                } else {
                    bgColor = '#E8F9F9';
                    iconHeight = '1.5em';
                    nameSize = '75%';
                }

                var spot = route[i];

                var spotIcon = $('<img>').attr('src', spot.icon).css({
                    'height': iconHeight,
                    'margin-right': '5px',
                    'border-radius': '50%',
                    'border': '2px solid black'
                });

                var spotName = spot.name;

                // TODO: Change icon to photo
                routeListGroup.append(
                    $('<li>').attr('class', 'list-group-item')
                        .css({
                            'background-color': bgColor,
                            'font-size': nameSize
                        })
                        .append(spotIcon)
                        .append(spotName)
                );
            }

            routeCard.append(routeListGroup);
            this.routeContainer.append(routeCard);
        });

        this.openRouteContainer();
        this.disableEvaluation();
    }

    updateEvaluater(hashtags, userId) {
        console.log('Evaluation: ', this.currentSelectedRoute);
        console.log('(Hashtags: ' + hashtags + ')');

        if (!this.currentSelectedRoute) {
            console.error('Error in updateEvaluater(): Invalid route!');
            return;
        }

        var spotAccordion = $('<div>').attr('id', 'accordion')
            .attr('role', 'tablist').attr('aria-multiselectable', 'true');

        var index = 0;

        this.currentSelectedRoute.forEach((spot) => {
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

        this.spotContainer.empty();
        this.spotContainer.append(spotAccordion);

        this.openSpotContainer();
        this.disableEvaluation();

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

    enableEvaluation() {
        this.evaluateButton.attr('disabled', false);
    }

    disableEvaluation() {
        this.evaluateButton.attr('disabled', true);
    }

    openMapContainer() {
        this.spotContainer.hide();
        this.routeContainer.hide();
        this.mapContainer.show();
    }

    openSpotContainer() {
        this.routeContainer.hide();
        this.mapContainer.hide();
        this.spotContainer.show();
    }

    openRouteContainer() {
        this.mapContainer.hide();
        this.spotContainer.hide();
        this.routeContainer.show();
    }
}
