import sqlite3
from flask import render_template
from routerconntest.models import *
from routerconntest.core import dbmanager

db = dbmanager.DBManager()


# Render: index.html
@app.route('/')
def render_index():
    print('>> Render: index.html')
    return render_template('index.html')


# Render: singin.html
@app.route('/signin')
def render_signin():
    print('>> Render: signin.html')
    return render_template('signin.html')


# Respond: From button click
@app.route('/update', methods=['GET'])
def respond_update():
    print('>> Request: (url)/update')

    # for debug. have to change after
    data_routes = [route_paris, route_france, route_europe]
    json_routes = json.dumps(data_routes)

    response = app.response_class(
        response=json_routes, status=200, mimetype='application/json')

    print('>> Response: %s' % json_routes)

    return response


@app.route('/evaluate', methods=['GET'])
def respond_evaluate():
    print('>> Request: (url)/update')

    hashtags = db.get_hashtag_list()
    json_hashtags = json.dumps(hashtags)

    return json_hashtags
