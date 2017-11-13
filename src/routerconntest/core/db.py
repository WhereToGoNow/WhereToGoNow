"""Module for handling the DB.

[Design]
(1) Table <SpotInfo> - Implemented
Table for information of each spot.

- id       : TEXT (Place ID)
- name     : TEXT (Spot name)
- latitude : REAL (Latitude)
- longitude: REAL (Longitude)
- staytime : REAL (Average time to enjoy the spot)
- address  : TEXT

* Primary key: id
* All fields are NOT NULL!

(2) Table <SpotEval> - Not implemented
(3) Table <UserInfo> - Not implemented
"""

import sqlite3

query_create_spotinfo = 'CREATE TABLE IF NOT EXISTS SpotInfo (' \
                        ' id        TEXT PRIMARY KEY NOT NULL,' \
                        ' name      TEXT NOT NULL,' \
                        ' latitude  REAL NOT NULL,' \
                        ' longitude REAL NOT NULL,' \
                        ' staytime  REAL NOT NULL,' \
                        ' address   TEXT NOT NULL' \
                        ')'

query_store_spotinfo = 'INSERT OR REPLACE INTO SpotInfo (' \
                       ' id, name, latitude, longitude, staytime, address' \
                       ') VALUES (?, ?, ?, ?, ?, ?)'

query_retrieve_spotinfo = 'SELECT * FROM SpotInfo WHERE placeId=?'


class DB(object):
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def close(self):
        try:
            self.connection.close()
        except sqlite3.Error:
            # Currently, do nothing when we failed to close.
            pass

    def create_spotinfo(self):
        self.run_query(query_create_spotinfo)

    def store_spotinfo(self, data):
        if data['address'] is None:
            address = 'Unknown'
        else:
            address = data['address']

        self.run_query(
            query_store_spotinfo,
            data['id'],
            data['name'],
            data['latitude'],
            data['longitude'],
            data['staytime'],
            address
        )

    def retrieve_spotinfo(self, id_):
        self.run_query(query_retrieve_spotinfo, id_)
        row = self.fetch_one()

        if row is None:
            return None
        else:
            return {
                'id': row[0],
                'name': row[1],
                'latitude': row[2],
                'longitude': row[3],
                'staytime': row[4],
                'address': row[5]
            }

    def run_query(self, query, *args):
        with self.connection:
            self.cursor.execute(query, args)

    def fetch_one(self):
        return self.cursor.fetchone()

    def fetch_all(self):
        return self.cursor.fetchall()


# Running this module directly try to create the DB & tables.
if __name__ == '__main__':
    path_db = '../static/data/spots.db'
    print('Trying to create %s...' % path_db)
    db = DB(sqlite3.connect(path_db))
    db.create_spotinfo()
    db.close()
