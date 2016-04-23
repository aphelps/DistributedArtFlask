from flask import render_template, session, redirect, url_for, current_app, request
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm, RGBForm
from connectors.client import create_client

from colour import Color

import hmtl.HMTLprotocol as HMTLprotocol

import json

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))


def set_client(app):
    if not app.da_client:
        app.da_client = create_client(app.address)
        return True
    return False


@main.route('/client', methods=['GET'])
def get_client():
    if set_client(current_app):
        return json.dumps("Created client")
    else:
        return json.dumps("Client was previously initalized")


@main.route('/rgb', methods=['GET', 'POST'])
def rgb():
    red = session.get('red', 0)
    green = session.get('green', 0)
    blue = session.get('blue', 0)
    form = RGBForm(red=red, green=green, blue=blue)

    if form.validate_on_submit():
        # Form submitted
        session['red'] = int(form.red.data)
        session['green'] = int(form.green.data)
        session['blue'] = int(form.blue.data)
        # session['red'] = form.color.data.red
        # session['blue'] = form.color.data.blue
        # session['green'] = form.color.data.green

        print("Sliders: %d" % form.red.data)

        return redirect(url_for('.rgb'))

    print("RGB: %f,%f,%f" % (red, green, blue))

    set_client(current_app)

    msg = HMTLprotocol.get_rgb_msg(HMTLprotocol.BROADCAST,
                                   HMTLprotocol.OUTPUT_ALL_OUTPUTS,
                                   int(red / 100.0 * 255),
                                   int(green / 100.0 * 255),
                                   int(blue / 100. * 255))
    current_app.da_client.send_and_ack(msg, False)
    return render_template('rgb.html',
                           form=form,
                           red=red,
                           green=green,
                           blue=blue)
