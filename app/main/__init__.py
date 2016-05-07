"""
This blueprint is for general views that do not directly interactive with any
connected devices.
"""

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
