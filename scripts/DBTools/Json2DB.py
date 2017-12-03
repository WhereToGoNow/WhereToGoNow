from __future__ import print_function

import json
import time

import googlemaps

import presets
from dbmanager import DBManager

api_key = presets.api_key['My Project']
db = DBManager(path='./spots_tools.db')
period_delay = 10
time_delay = 5
client = googlemaps.Client(api_key)
options_detail = {'language': 'en'}

with open('./spots_more.json', 'rb') as p:
    data_spots = json.load(p)

list_ids = [s['place_id'] for s in data_spots.values()]

for i in xrange(len(list_ids)):
    if i > 0 and i % period_delay == 0:
        print('Delaying: %d seconds...' % time_delay, end=' ')
        time.sleep(time_delay)
        print('Success!')

    print('Searching the spot with id %s...' % list_ids[i], end=' ')
    response_detail = getattr(client, 'place')(
        list_ids[i], **options_detail)

    if response_detail['status'] == 'OK':
        print('Success!')
    else:
        print('Failed!')
        continue

    info = response_detail['result']

    print('Inserting the result into SpotInfo DB...', end=' ')

    db.run_query(
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

print('Done!')
