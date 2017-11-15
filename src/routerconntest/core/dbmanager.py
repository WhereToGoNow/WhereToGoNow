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
        self.connection = sqlite3.connect('../static/data/spots.db')
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
        self.run_query('SELECT name FROM HashtagList')
        return self.fetch_all()
