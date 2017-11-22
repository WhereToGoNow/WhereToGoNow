from flask import render_template, request
from flask_login import login_user, logout_user

from routerconntest.core import dbmanager
from routerconntest.models import *

db = dbmanager.DBManager()


# Render: index.html
@app.route('/')
def render_index():
    print('>> Render: index.html')
    return render_template('index.html')


# Respond: From button click
@app.route('/update', methods=['POST'])
def respond_update():
    print('>> Request: (url)/update')

    contents = request.form
    print contents

    # for debug. have to change after
    data_routes = [route_paris, route_france, route_europe]
    json_routes = json.dumps(data_routes)

    response = app.response_class(
        response=json_routes, status=200, mimetype='application/json')

    # print('>> Response: %s' % json_routes)

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

    if db.update_hashtag(contents['userId'], contents['spotId'],
                         contents['hashtagId'], contents['updateType']):
        return app.response_class(
            response={'result': True},
            status=200,
            mimetype='application/json'
        )

    return app.response_class(
        response=json.dumps({'result': False}),
        status=403
    )


@app.route('/sign-up', methods=['POST'])
def respond_sign_up():
    print('>> Request: (url)/sign-up')

    id_ = request.json['id']
    password = request.json['password']
    data_result = {'success': False, 'msg': ''}

    if sign_manager.add_user(id_, password):
        login_user(User(id_))
        data_result['success'] = True
        print('>> User %s: Sign-up success' % id_)
    else:
        data_result['success'] = False
        data_result['msg'] = 'User "%s" already exists!' % id_
        print('>> User %s: Sign-up failed' % id_)

    return app.response_class(
        response=json.dumps(data_result),
        status=200,
        mimetype='application/json'
    )


@app.route('/sign-in', methods=['POST'])
def respond_sign_in():
    print('>> Request: (url)/sign-in')

    id_ = request.json['id']
    password = request.json['password']
    data_result = {'success': False, 'msg': ''}

    if sign_manager.authenticate_user(id_, password):
        login_user(User(id_))
        data_result['success'] = True
        print('>> User %s: Sign-in success' % id_)
    else:
        data_result['success'] = False
        data_result['msg'] = 'Id or password does not match!'
        print('>> User %s: Sign-in failed' % id_)

    return app.response_class(
        response=json.dumps(data_result),
        status=200,
        mimetype='application/json'
    )


@app.route('/sign-out', methods=['POST'])
def respond_sign_out():
    print('>> Request: (url)/sign-out')

    logout_user()
    data_result = {'success': True}

    print('>> Sign-out success')

    return app.response_class(
        response=json.dumps(data_result),
        status=200,
        mimetype='application/json'
    )
