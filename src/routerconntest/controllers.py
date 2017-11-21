from flask import render_template, request
from flask_login import login_user

from routerconntest.core import dbmanager
from routerconntest.models import *

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

    #print('>> Response: %s' % json_routes)

    return response


@app.route('/hashtags', methods=['GET'])
def respond_hashtags():
    print('>> Request: (url)/hashtags')

    hashtags = db.get_hashtag_list()
    json_hashtags = json.dumps(hashtags)

    return json_hashtags


@app.route('/spots', methods=['GET'])
def respond_spots():
    print('>> Request: (url)/spots')

    spots = db.get_spot_list()
    json_spots = json.dumps(spots)

    return json_spots


@app.route('/hashtags/<userId>', methods=['GET'])
def respond_hashtag_list_by_user_id(userId):
    print('>> Request: (url)/hashtags/<userId>')

    hashtags = db.get_hashtag_list_by_user_id(userId)
    json_hashtags = json.dumps(hashtags)

    return json_hashtags


@app.route('/hashtags/update', methods=['POST'])
def respond_hashtags_update():
    print('>> Request: (url)/hashtags/update')

    contents = request.form
    print contents

    if db.update_hashtag(contents['userId'], contents['spotId'], contents['hashtagId'], contents['updateType']):
        return app.response_class(response={'result': True}, status=200, mimetype='application/json')

    return app.response_class(response={'result': False}, status=403)


@app.route('/signin/signup', methods=['POST'])
def respond_signup():
    print('>> Request: (url)/signin/signup')

    id_ = request.json['id']
    password = request.json['password']

    if sign_manager.add_user(id_, password):
        login_user(User(id_))
        print('>> User %s: Sign-up success' % id_)
        data_result = {'result': True}
    else:
        print('>> User %s: Sign-up failed' % id_)
        data_result = {'result': False}

    json_result = json.dumps(data_result)

    response = app.response_class(
        response=json_result, status=200, mimetype='application/json'
    )

    return response


@app.route('/signin/signin', methods=['POST'])
def respond_signin():
    print('>> Request: (url)/signin/signin')

    id_ = request.json['id']
    password = request.json['password']

    if sign_manager.authenticate_user(id_, password):
        login_user(User(id_))
        print('>> User %s: Sign-in success' % id_)
        data_result = {'result': True}
    else:
        print('>> User %s: Sign-in failed' % id_)
        data_result = {'result': False}

    json_result = json.dumps(data_result)

    response = app.response_class(
        response=json_result, status=200, mimetype='application/json'
    )

    return response
