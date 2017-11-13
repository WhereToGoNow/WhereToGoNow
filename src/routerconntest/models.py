import json
from math import sin, cos, asin, sqrt

from routerconntest import app
from routerconntest.core import router


def calc_distance(lat_1, lng_1, lat_2, lng_2):
    """Calculate the distance between two points.
    (See https://en.wikipedia.org/wiki/Haversine_formula)
    """
    s_lat = sin((lat_1 - lat_2) / 2.0) ** 2
    s_lng = sin((lng_1 - lng_2) / 2.0) ** 2
    h = min(s_lat + cos(lat_1) * cos(lat_2) * s_lng, 1.0)
    r = 6371  # radius of earth (km)

    return 2.0 * r * asin(sqrt(h))


class RouteGenerator(object):
    def __init__(self, path_spots, speed=8.0):
        # extract info.
        with app.open_resource(path_spots) as p:
            self.info_spots = json.load(p)

        self.name_spots = self.info_spots.keys()
        self.num_spots = len(self.name_spots)
        self.id_spots = []
        self.lat_spots = []
        self.lng_spots = []
        self.rating_spots = []

        for v in range(self.num_spots):
            info = self.info_spots[self.name_spots[v]]

            self.id_spots.append(info['place_id'])
            self.lat_spots.append(info['location']['lat'])
            self.lng_spots.append(info['location']['lng'])

            rating = info['rating']

            if rating is None:
                self.rating_spots.append(3)
            else:
                self.rating_spots.append(rating)

        # initialize graph & router
        self.graph = router.Graph(self.num_spots)
        self.router = router.Router(self.graph)

        for v in range(self.num_spots):
            self.graph.time_nodes[v] = 1
            self.graph.eval_nodes[v] = self.rating_spots[v]

            for v_next in range(v + 1, self.num_spots):
                distance = calc_distance(
                    lat_1=self.lat_spots[v],
                    lng_1=self.lng_spots[v],
                    lat_2=self.lat_spots[v_next],
                    lng_2=self.lng_spots[v_next]
                )

                time = distance / float(speed)

                self.graph.time_edges[v][v_next] = time
                self.graph.time_edges[v_next][v] = time

    def generate_route(self, v_start, v_end, length_max=None, time_max=None):
        if length_max is None:
            length_max = self.num_spots

        if time_max is None:
            time_max = float('inf')

        path = self.router.find_best_path(v_start, v_end, length_max, time_max)

        return [{
            'name': self.name_spots[v],
            'id': self.id_spots[v],
            'lat': self.lat_spots[v],
            'lng': self.lng_spots[v]
        } for v in path.nodes]


# Pre-compute the paths for testing
# (will be removed later)
route_paris = RouteGenerator(
    path_spots='static/data/spots_paris.json',
    speed=8.0
).generate_route(0, 1, time_max=24 * 2)

route_france = RouteGenerator(
    path_spots='static/data/spots_france.json',
    speed=60.0
).generate_route(0, 1, time_max=24 * 9)

route_europe = RouteGenerator(
    path_spots='static/data/spots_europe.json',
    speed=60.0
).generate_route(0, 1, time_max=24 * 12)
