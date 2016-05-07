
from flask import render_template, session, redirect, url_for, current_app, request
from . import api
from .. import auto

from connectors.client import get_client

import json

#
# Basic REST API
#
@api.route('/client', methods=['GET'])
@auto.doc()
def client():
    if not current_app.client:
        current_app.client = get_client(current_app.address)

    if current_app.client.is_connected():
        return json.dumps("Client was already connected")
    else:
        if current_app.client.connect():
            return json.dumps("Client is now connected")
        else:
            return json.dumps("Client failed to connect")


@api.route('/rgb/set', methods=['GET'])
@auto.doc()
def set_rgb():
    client()

    session['red'] = int(request.args.get('red', 0))
    session['green'] = int(request.args.get('green', 0))
    session['blue'] = int(request.args.get('blue', 0))

    current_app.client.send_rgb(session['red'],
                                session['green'],
                                session['blue'])

    return json.dumps({"red":session['red'],
                       "green":session['green'],
                       "blue":session['blue']})

@api.route('/clear_programs')
@auto.doc()
def clear_programs():
    client()

    current_app.client.send_clear_programs()
    return json.dumps("Cleared")
