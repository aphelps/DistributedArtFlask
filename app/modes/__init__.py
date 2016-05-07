"""
This blueprint is for the views for the various modes and program commands that
can be sent to the connected devices.
"""

from flask import Blueprint

modes = Blueprint('modes', __name__)

from . import views
