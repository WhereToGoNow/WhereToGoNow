import json
import sqlite3

from routerconntest.lib.db import DB

if __name__ == '__main__':
    print('Creating spots.db...')
    path_db = 'spots.db'
    db = DB(sqlite3.connect(path_db))
    db.create_spotinfo()

    print('Moving data in spots.json to spots.db...')

    with open('spots.json', 'rb') as p:
        info_spots = json.load(p)

    for name in info_spots:
        print('- Storing %s...' % name)
        info = info_spots[name]

        data = {
            'id': info['place_id'],
            'name': info['name'],
            'latitude': info['location']['lat'],
            'longitude': info['location']['lng'],
            'staytime': 1,
            'address': info['address']
        }

        db.store_spotinfo(data)
