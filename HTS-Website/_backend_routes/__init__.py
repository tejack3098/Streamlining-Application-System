from flask import Blueprint

backendapp = Blueprint('backendapp', __name__)

from . import views

