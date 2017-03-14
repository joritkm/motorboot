from flask import Blueprint

bp = Blueprint('bootfiles', __name__)

from . import views
