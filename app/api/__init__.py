"""
This blueprint is for straight-up command endpoints that do not present
HTML views.
"""

from flask import Blueprint

api = Blueprint('api', __name__)

from . import routes
