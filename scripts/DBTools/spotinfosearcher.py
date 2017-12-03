from __future__ import print_function

import time
import urllib

import googlemaps

import presets
from dbmanager import DBManager


# XXX: Wikipedia API works only when we give 'precise' information
def search_wiki(name):
    head = 'https://en.wikipedia.org/w/api.php'

    args = urllib.urlencode({
        'action': 'query',
        'prop': 'extracts',
        'rvprop': 'content',
        'rvsection': '0',
        'titles': urllib.quote_plus(name)
    })

    url = head + '?' + args
    print(url)


class SpotInfoSearcher(object):
    def __init__(self, api_key, path_db, period_delay=10, time_delay=5,
                 num_spots_max=20):
        self.client = googlemaps.Client(api_key)
        self.db = DBManager(path='./spots_tools.db')
        self.period_delay = period_delay
        self.time_delay = time_delay
        self.num_spots_max = num_spots_max

    def search(self, options_radar, options_detail):
        # (1) find place ids first
        print('Searching the available places (options: %s)...' % options_radar,
              end=' ')
        response = getattr(self.client, 'places_radar')(**options_radar)

        if response['status'] == 'OK':
            print('Success!')
        else:
            print('Failed!')
            return

        list_ids = [spot['place_id'] for spot in response['results']]
        num_spots = min(len(list_ids), self.num_spots_max)

        # (2) find detail info. of each spot
        for i in xrange(num_spots):
            if i > 0 and i % self.period_delay == 0:
                print('Delaying: %d seconds...' % self.time_delay, end=' ')
                time.sleep(self.time_delay)
                print('Success!')

            print('Searching the spot with id %s...' % list_ids[i], end=' ')
            response_detail = getattr(self.client, 'place')(
                list_ids[i], **options_detail)

            if response_detail['status'] == 'OK':
                print('Success!')
            else:
                print('Failed!')
                continue

            info = response_detail['result']

            # (3) get the description from Wikipedia

            # (4) insert the result into SpotInfo DB
            print('Inserting the result into SpotInfo DB...', end=' ')

            self.db.run_query(
                'INSERT OR REPLACE INTO SpotInfo ('
                ' id, name, latitude, longitude, types, rating, address,'
                ' website, phone, vicinity, url, icon, description'
                ') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                info['place_id'],
                info['name'],
                info['geometry']['location']['lat'],
                info['geometry']['location']['lng'],
                '|'.join(info['types']),
                info.get('rating', 3),
                info.get('address'),
                info.get('website'),
                info.get('international_phone_number'),
                info.get('vicinity'),
                info.get('url'),
                info.get('icon'),
                None
            )

            print('Success!')


if __name__ == '__main__':
    searcher = SpotInfoSearcher(
        api_key=presets.api_key['Avant-WhereToGoNow'],
        path_db='spots.db'
    )

    # find the spots inside Rome
    for type_ in presets.list_types:
        searcher.search(
            options_radar={
                'location': {'lat': 41.895165, 'lng': 12.496506},  # Rome
                'radius': 4000,
                'type': type_
            },
            options_detail={
                'language': 'en'
            }
        )

    print('Done!')
