from flask import render_template

from routerconntest.models import *

# Render: index.html


@app.route('/')
def render_index():
    print('>> Render: index.html')
    return render_template('index.html')


# Respond: From button click
@app.route('/update', methods=['GET'])
def respond_update():
    print('>> Request: (url)/update')

    # for debug. have to change after
    data_routes = [route_paris, route_france, route_europe]
    # json_routes = json.dumps([json.dumps(data) for data in data_routes])
    # We can just dump the whole list...
    # (So we parse the data just once in the client.)
    json_routes = json.dumps(data_routes)

    response = app.response_class(
        response=json_routes,
        status=200,
        mimetype='application/json'
    )

    print('>> Response: %s' % json_routes)

    return response
