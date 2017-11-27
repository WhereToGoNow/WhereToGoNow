"""Simple class for managing the DB easily.

[Example]
import sqlite3

john_id, john_password, john_name = 'User1234', 'abc12345', 'John'
db = DBManager(sqlite3.connect('path_to_db.db'))

# insert the new information
db.run_query('INSERT INTO UserInfo (id, password, name) VALUES(?, ?, ?)',
             john_id, john_password, john_name)

# retrieve the information
paul_id, paul_password = 'Paul95', 'xyz123'
db.run_query('SELECT name FROM UserInfo WHERE id=? AND password=?',
             paul_id, paul_password)
row_match = db.fetch_one()
paul_name = row_match[0]

# close the DB
db.close()
"""

import sqlite3


class DBManager(object):
    def __init__(self):
        self.connection = sqlite3.connect(
            'wheretogonow/static/data/spots.db',
            check_same_thread=False  # flask_login uses multiple threads
        )
        self.connection.row_factory = lambda c, r: dict(
            [(col[0], r[idx]) for idx, col in enumerate(c.description)])

        self.cursor = self.connection.cursor()

    def close(self):
        """Close the connection."""
        try:
            self.connection.close()
        except sqlite3.Error:
            # suppress the error
            pass

    def run_query(self, query, *args):
        """Run the query with the given args."""
        with self.connection:
            self.cursor.execute(query, args)

    def fetch_one(self):
        """Retrieve one matching row."""
        return self.cursor.fetchone()

    def fetch_all(self):
        """Retrieve all matching rows."""
        return self.cursor.fetchall()

    def get_hashtag_list(self):
        self.run_query('SELECT * FROM HashtagList')
        return self.fetch_all()

    def get_spot_list(self):
        self.run_query('SELECT * FROM SpotInfo')
        return self.fetch_all()

    def get_spot_info(self):
        self.run_query('SELECT * FROM SpotInfo')
        return self.fetch_all()

    def get_route_info(self, id_start, id_end):
        self.run_query('SELECT time, distance FROM RouteInfo'
                       ' WHERE startId=? AND endId=?',
                       id_start, id_end)
        return self.fetch_one()

    def get_hashtag_list_by_user_id(self, userId):
        self.run_query('SELECT userId, spotId, hashtagId FROM SpotEval'
                       ' WHERE userId=?',
                       userId)
        return self.fetch_all()

    def update_hashtag(self, userId, spotId, hashtagId, updateType):
        print userId, spotId, hashtagId, updateType

        if updateType == 'remove':
            print 'delete'
            self.run_query('DELETE FROM SpotEval'
                           ' WHERE userId=? and spotId=? and hashtagId=?',
                           userId, spotId, hashtagId)
        elif updateType == 'update':
            print 'insert'
            self.run_query(
                'INSERT INTO SpotEval VALUES (NULL, ?, ?, ?)', userId, spotId,
                hashtagId)

        return True
