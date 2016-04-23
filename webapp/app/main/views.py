from flask import render_template, session, redirect, url_for, current_app, request
from .. import db, auto
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm, RGBForm

from connectors.client import get_client

import json



@main.route('/documentation')
def documentation():
    return auto.html()


@main.route('/', methods=['GET', 'POST'])
@auto.doc()
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


@main.route('/client', methods=['GET'])
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


@main.route('/rgb', methods=['GET', 'POST'])
@auto.doc()
def rgb():
    client()

    red = session.get('red', 0)
    green = session.get('green', 0)
    blue = session.get('blue', 0)
    form = RGBForm(red=(red / 255.0 * 100),
                   green=(green / 255.0 * 100),
                   blue=(blue / 255.0 * 100))

    if form.validate_on_submit():
        # Form submitted
        session['red'] = int(form.red.data) / 100.0 * 255
        session['green'] = int(form.green.data) / 100.0 * 255
        session['blue'] = int(form.blue.data) / 100.0 * 255

        current_app.client.send_rgb(session['red'],
                                    session['green'],
                                    session['blue'])

        # Redirect will send back to here and update the display
        return redirect(url_for('.rgb'))

    return render_template('rgb.html',
                           form=form,
                           red=red,
                           green=green,
                           blue=blue)

@main.route('/snake', methods=['GET', 'POST'])
@auto.doc()
def snake():
    client()

    red = session.get('red', 0)
    green = session.get('green', 0)
    blue = session.get('blue', 0)

    form = RGBForm(red=(red / 255.0 * 100),
                   green=(green / 255.0 * 100),
                   blue=(blue / 255.0 * 100))

    if form.validate_on_submit():
        # Form submitted
        session['red'] = int(form.red.data) / 100.0 * 255
        session['green'] = int(form.green.data) / 100.0 * 255
        session['blue'] = int(form.blue.data) / 100.0 * 255
        session['period'] = 100
        session['colormode'] = 0

        current_app.client.send_snake((session['red'],
                                       session['green'],
                                       session['blue']),
                                       session['period'],
                                       session['colormode']
                                      )

        # Redirect will send back to here and update the display
        return redirect(url_for('.snake'))

    return render_template('snake.html',
                           form=form,
                           red=red,
                           green=green,
                           blue=blue)


#
# Basic REST API
#

@main.route('/rgb/set', methods=['GET'])
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

@main.route('/clear_programs')
@auto.doc()
def clear_programs():
    client()

    current_app.client.send_clear_programs()
    return json.dumps("Cleared")
