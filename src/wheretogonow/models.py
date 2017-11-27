from math import sin, cos, asin, sqrt

from wheretogonow import app
from wheretogonow.core.dbmanager import DBManager
from wheretogonow.core.router import Router, Graph
from wheretogonow.core.signmanager import SignManager, User


# ==================== Routing ====================

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
    def __init__(self):
        self.db = DBManager()
        self.info_spots = self.db.get_spot_info()
        self.num_spots = len(self.info_spots)

        # 0th vertex: starting point
        # 1th vertex: ending point
        # ith vertex (i >= 2) : spots
        # Setting like this prevents re-generating the whole graph every time.
        self.graph = Graph(self.num_spots + 2)
        self.router = Router(self.graph)

        for i_curr in xrange(self.num_spots):
            v_curr = i_curr + 2
            id_curr = self.info_spots[i_curr]['id']
            eval_curr = self.info_spots[i_curr]['rating']

            self.graph.time_nodes[v_curr] = 3  # 3 hours for each spot
            self.graph.eval_nodes[v_curr] = eval_curr

            for i_next in xrange(i_curr, self.num_spots):
                v_next = i_next + 2
                id_next = self.info_spots[i_next]['id']

                self.graph.time_edges[v_curr][v_next] \
                    = self.db.get_route_info(id_curr, id_next)['time'] / 3600.0

                self.graph.time_edges[v_next][v_curr] \
                    = self.db.get_route_info(id_next, id_curr)['time'] / 3600.0

    def generate_route(self, lat_start, lng_start, lat_end, lng_end,
                       length_max=None, time_max=None):
        if length_max is None:
            length_max = self.num_spots

        if time_max is None:
            time_max = float('inf')

        speed = 40.0  # km/h

        # update the times between starting point <-> each spot
        # and each spot <-> ending point
        for i in xrange(self.num_spots):
            v = i + 2
            lat_v = self.info_spots[i]['latitude']
            lng_v = self.info_spots[i]['longitude']

            time_start = calc_distance(
                lat_start, lng_start, lat_v, lng_v) / speed

            time_end = calc_distance(
                lat_end, lng_end, lat_v, lng_v) / speed

            self.graph.time_edges[0][v] = time_start
            self.graph.time_edges[v][0] = time_start
            self.graph.time_edges[1][v] = time_end
            self.graph.time_edges[v][1] = time_end

        plist = self.router.find_best_path(0, 1, 4, length_max + 2, time_max)
        result = []

        for path in plist:
            route = []

            for v in path.nodes[1:-1]:
                info = self.info_spots[v - 2]

                route.append({
                    'name': info['name'],
                    'id': info['id'],
                    'lat': info['latitude'],
                    'lng': info['longitude'],
                    'icon': info['icon']
                })

            result.append(route)

        return result


route_generator = RouteGenerator()

# ==================== Signing ====================

sign_manager = SignManager()
sign_manager.init_app(app)


# Required by flask_login: Used when reloading the user from the session.
# If the user exists -> Return 'User' instance / Otherwise -> Return None
@sign_manager.user_loader
def user_loader(id_):
    if sign_manager.search_user(id_):
        print('>> user_loader: success')
        return User(id_)
    else:
        print('>> user_loader: failed')
        return None
