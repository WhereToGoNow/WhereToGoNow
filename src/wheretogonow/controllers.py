import json

from flask import render_template, request
from flask_login import login_user, logout_user

from wheretogonow import app
from wheretogonow.core import dbmanager
from wheretogonow.models import route_generator, sign_manager, User

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

    loc_start = request.json['start']
    loc_end = request.json['end']
    print('>> Start: %s' % loc_start)
    print('>> End: %s' % loc_end)

    data_routes = route_generator.generate_route(
        lat_start=loc_start['lat'],
        lng_start=loc_start['lng'],
        lat_end=loc_end['lat'],
        lng_end=loc_end['lng'],
        length_max=6 + 1,
        time_max=24 + 6
    )

    print('>> Found %d routes' % len(data_routes))
    json_routes = json.dumps(data_routes)

    response = app.response_class(
        response=json_routes, status=200, mimetype='application/json')

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

    list_spots = db.get_spot_list()
    result = []

    for spot in list_spots:
        result.append({
            'name': spot['name'],
            'id': spot['id'],
            'lat': spot['latitude'],
            'lng': spot['longitude'],
            'icon': spot['icon']
        })

    return json.dumps(result)


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
