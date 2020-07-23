from flask import  Blueprint


empapp = Blueprint('empapp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='static')

from . import emp_views