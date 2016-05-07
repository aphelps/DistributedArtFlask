#
# Basic REST API for sending commands to distributed art modules
#

from flask import session, current_app, request
from . import api
from .. import auto

from connectors import connected

import json

@api.route('/rgb/set', methods=['GET'])
@auto.doc()
@connected
def set_rgb():
    session['red'] = int(request.args.get('red', 0))
    session['green'] = int(request.args.get('green', 0))
    session['blue'] = int(request.args.get('blue', 0))

    current_app.client.state.send_rgb(session['red'],
                                      session['green'],
                                      session['blue'])

    return json.dumps({"red":session['red'],
                       "green":session['green'],
                       "blue":session['blue']})


@api.route('/clear_programs')
@auto.doc()
@connected
def clear_programs():
    current_app.client.state.send_clear_programs()
    return json.dumps("Cleared")
