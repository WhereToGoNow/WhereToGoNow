from __future__ import print_function

import math
import sqlite3
import time

import googlemaps

import presets
from dbmanager import DBManager


def calc_distance(lat_1, lng_1, lat_2, lng_2):
    """Calculate the distance between two points.
    (See https://en.wikipedia.org/wiki/Haversine_formula)
    """
    lat_1, lng_1 = lat_1 * math.pi / 180.0, lng_1 * math.pi / 180.0
    lat_2, lng_2 = lat_2 * math.pi / 180.0, lng_2 * math.pi / 180.0

    hav_lat = math.sin((lat_1 - lat_2) / 2.0) ** 2
    hav_lng = math.sin((lng_1 - lng_2) / 2.0) ** 2
    h = min(hav_lat + math.cos(lat_1) * math.cos(lat_2) * hav_lng, 1.0)
    r = 6371000.0  # radius of earth (m)

    return 2.0 * r * math.asin(math.sqrt(h))


class RouteInfoSearcher(object):
    def __init__(self, api_key, path_db, size_matrix=10, time_delay=5):
        self.client = googlemaps.Client(api_key)
        self.db = DBManager(sqlite3.connect(path_db))
        self.size_matrix = size_matrix
        self.time_delay = time_delay

        # extract id & location from SpotInfo DB
        print('Extracting spots\' info from SpotInfo DB...', end=' ')
        self.db.run_query('SELECT id, latitude, longitude FROM SpotInfo')
        list_rows = self.db.fetch_all()
        print('Success!')

        # build the objects used for searching
        self.num_spots = len(list_rows)
        self.list_ids = [row[0] for row in list_rows]
        self.list_lats = [row[1] for row in list_rows]
        self.list_lngs = [row[2] for row in list_rows]

        # list of (index_min, index_max + 1) for each submatrix
        self.list_ranges = [
            (i, min(i + self.size_matrix, self.num_spots))
            for i in xrange(0, self.num_spots, self.size_matrix)
        ]

    def try_transit(self, info_routes, range_start, range_end):
        print('- Trying the transit mode...', end=' ')

        input_start = ['place_id:%s' % self.list_ids[i]
                       for i in xrange(*range_start)]

        input_end = ['place_id:%s' % self.list_ids[i]
                     for i in xrange(*range_end)]

        response = getattr(self.client, 'distance_matrix')(
            origins=input_start,
            destinations=input_end,
            units='metric',
            mode='transit',
            transit_routing_preference='less_walking'
        )

        num_tries, num_fails = 0, 0

        if response['status'] == 'OK':
            for i in xrange(*range_start):
                row = response['rows'][i - range_start[0]]['elements']

                for j in xrange(*range_end):
                    item = row[j - range_end[0]]
                    num_tries += 1

                    if item['status'] == 'OK':
                        info_routes[i][j] = {
                            'time': item['duration']['value'],
                            'distance': item['distance']['value']
                        }
                    else:
                        num_fails += 1

        print('%d / %d failed!' % (num_fails, num_tries))
        return num_fails == 0

    def try_walking(self, info_routes, range_start, range_end):
        print('- Trying the walking mode...', end=' ')
        num_tries, num_fails = 0, 0

        for i in xrange(*range_start):
            for j in xrange(*range_end):
                if info_routes[i][j] is None:
                    response = getattr(self.client, 'directions')(
                        origin='place_id:%s' % self.list_ids[i],
                        destination='place_id:%s' % self.list_ids[j],
                        units='metric',
                        mode='walking'
                    )

                    num_tries += 1

                    if response and response[0]['legs']:
                        item = response[0]['legs'][0]

                        info_routes[i][j] = {
                            'time': item['duration']['value'],
                            'distance': item['distance']['value']
                        }
                    else:
                        num_fails += 1

        print('%d / %d failed!' % (num_fails, num_tries))
        return num_fails == 0

    def try_guessing(self, info_routes, range_start, range_end):
        print('- Trying to guess using the haversine formula...', end=' ')
        num_tries = 0

        for i in xrange(*range_start):
            for j in xrange(*range_end):
                if info_routes[i][j] is None:
                    distance = calc_distance(
                        self.list_lats[i], self.list_lngs[i],
                        self.list_lats[j], self.list_lngs[j]
                    )

                    num_tries += 1

                    info_routes[i][j] = {
                        'time': distance / 1.23,  # walking speed: 1.23m/s,
                        'distance': distance
                    }

        print('Success! (%d)' % num_tries)

    def search(self):
        info_routes = [[None] * self.num_spots for _ in xrange(self.num_spots)]

        try:
            for range_start in self.list_ranges:
                for range_end in self.list_ranges:
                    print('Searching (%d ~ %d) X (%d ~ %d):'
                          % (range_start[0], range_start[1] - 1,
                             range_end[0], range_end[1] - 1))

                    # try the transit mode (i.e public transportations)
                    if self.try_transit(info_routes, range_start, range_end):
                        continue

                    # try the walking mode
                    if self.try_walking(info_routes, range_start, range_end):
                        continue

                    # try to guess using the haversine formula
                    self.try_guessing(info_routes, range_start, range_end)

                    print('Delaying: %d seconds...' % self.time_delay, end=' ')
                    time.sleep(self.time_delay)
                    print('Success!')
        except googlemaps.exceptions.Timeout:
            print('\nTimeout! We\'ll just guess the remaining routes.')
            range_whole = (0, self.num_spots)
            self.try_guessing(info_routes, range_whole, range_whole)

        # insert the result into RouteInfo DB
        print('Inserting the result into RouteInfo DB:')

        for i in xrange(self.num_spots):
            for j in xrange(self.num_spots):
                print('- Route %d -> %d...' % (i, j), end=' ')

                self.db.run_query(
                    'INSERT OR REPLACE INTO RouteInfo ('
                    ' startId, endId, time, distance'
                    ') VALUES (?, ?, ?, ?)',
                    self.list_ids[i],
                    self.list_ids[j],
                    info_routes[i][j]['time'],
                    info_routes[i][j]['distance']
                )

                print('Success!')


if __name__ == '__main__':
    searcher = RouteInfoSearcher(
        api_key=presets.api_key['Avant-WTGN-2'],
        path_db='spots.db'
    )

    searcher.search()
    print('Done!')
