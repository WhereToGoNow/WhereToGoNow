"""Sign-in (and sign-up) manager.
See https://github.com/maxcountryman/flask-login
"""

import flask_login

from routerconntest.core.dbmanager import DBManager


# Class which represents a single user: Used by flask_login.
class User(flask_login.UserMixin):
    def __init__(self, id_):
        self.id = id_

    def __repr__(self):
        return '[User %s]' % self.id


# Class which wraps LoginManager provied by flask_login.
class SignManager(flask_login.LoginManager):
    def __init__(self, *args, **kwargs):
        super(SignManager, self).__init__(*args, **kwargs)
        self.db = DBManager()

    def search_user(self, id_):
        """Match id only (not password) -> Confirm that the user exists."""
        self.db.run_query('SELECT * FROM UserInfo WHERE id=?', id_)
        row_match = self.db.fetch_one()

        if row_match is None:
            return False
        else:
            return True

    def authenticate_user(self, id_, password):
        """Match both id and password -> Allows the user to sign in."""
        self.db.run_query('SELECT * FROM UserInfo WHERE id=? AND password=?',
                          id_, password)
        row_match = self.db.fetch_one()

        if row_match is None:
            return False
        else:
            return True

    def add_user(self, id_, password):
        if self.search_user(id_):
            return False

        self.db.run_query('INSERT INTO UserInfo (id, password) VALUES (?, ?)',
                          id_, password)
        return True
