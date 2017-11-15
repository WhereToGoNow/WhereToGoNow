import sqlite3


class DBManager(object):
    def __init__(self, connection):
        self.connection = connection
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
