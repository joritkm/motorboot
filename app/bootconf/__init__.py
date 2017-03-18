from flask import Blueprint

bp = Blueprint('bootconf', __name__)


from . import api
