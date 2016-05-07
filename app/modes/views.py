from flask import render_template, session, redirect, url_for, current_app, request
from .. import auto
from . import modes
from .forms import RGBForm
from connectors import connected

@modes.route('/rgb', methods=['GET', 'POST'])
@auto.doc()
@connected
def rgb():
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

        current_app.client.state.rgb(session['red'],
                                    session['green'],
                                    session['blue'])

        # Redirect will send back to here and update the display
        return redirect(url_for('.rgb'))

    return render_template('rgb.html',
                           form=form,
                           red=red,
                           green=green,
                           blue=blue)


@modes.route('/snake', methods=['GET', 'POST'])
@auto.doc()
@connected
def snake():
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

        current_app.client.state.snake((session['red'],
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


