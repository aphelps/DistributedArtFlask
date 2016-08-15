from flask import render_template, session, redirect, url_for, current_app, request
from .. import auto
from . import modes
from .forms import RGBForm, SnakeForm
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

        current_app.state.rgb(session['red'],
                                    session['green'],
                                    session['blue'])

        # Redirect will send back to here and update the display
        return redirect(url_for('.rgb'))

    return render_template('modes/rgb.html',
                           form=form,
                           red=red,
                           green=green,
                           blue=blue)

@modes.route('/blink', methods=['GET', 'POST'])
@auto.doc()
@connected
def blink():
    pass


@modes.route('/snake', methods=['GET', 'POST'])
@auto.doc()
@connected
def snake():
    red = session.get('red', 0)
    green = session.get('green', 0)
    blue = session.get('blue', 0)
    period = session.get('period', 100)
    colormode = session.get('colormode', 0)

    form = SnakeForm(red=(red / 255.0 * 100),
                     green=(green / 255.0 * 100),
                     blue=(blue / 255.0 * 100),
                     period=period,
                     colormode=colormode)

    if form.validate_on_submit():
        # Form submitted
        session['red'] = int(form.red.data) / 100.0 * 255
        session['green'] = int(form.green.data) / 100.0 * 255
        session['blue'] = int(form.blue.data) / 100.0 * 255
        session['period'] = int(form.period.data)
        session['colormode'] = int(form.colormode.data)

        print("XXXX: period=%d mode=%d" % (session['period'], session['colormode']))

        current_app.state.snake((session['red'],
                                 session['green'],
                                 session['blue']),
                                session['period'],
                                session['colormode']
                                )

        # Redirect will send back to here and update the display
        return redirect(url_for('.snake'))

    return render_template('modes/snake.html',
                           form=form,
                           red=red,
                           green=green,
                           blue=blue,
                           period=period,
                           colormode=colormode)


