#!/usr/local/bin/python3

# AUTH/INIT

import flask

auth_blueprint = flask.Blueprint('auth', __name__, template_folder="templates")

from . import views  # . is auth