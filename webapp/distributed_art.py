#!/usr/bin/env python

from flask import Flask, render_template, session, redirect, url_for, flash, current_app
from flask.ext.script import Manager, Server
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

from connectors.client import create_client

from app.server import DAServer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

manager = Manager(app)
# manager.add_command("run", DAServer())


bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    print("Client: %s" % current_app.da_client)

    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


@manager.option("-a", "--address", default="localhost", help="Address of DA Command Server to connect to")
def run(address):
    options = {}

    app.da_client = create_client(address)

    app.run()

if __name__ == '__main__':

    print("STARTING")
    manager.run()
