from flask import Blueprint


adminapp = Blueprint('adminapp', __name__,
	template_folder='templates',
    static_folder='static',
    static_url_path='static')

from . import admin_views