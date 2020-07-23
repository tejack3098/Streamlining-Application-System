from flask import Flask, render_template, request,session, redirect, url_for, jsonify
import requests, json, base64, pymongo
from flask_cors import CORS

# Blueprints Import
from _backend_routes import backendapp
from _admin import adminapp
from _emp import empapp



def page_not_found(e):
  return render_template('404.html'), 404


app = Flask(__name__,template_folder='_templates',static_folder='_static') # Main App
CORS(app)   
app.secret_key="abcdffgdefgac"

# Blueprints of AdminApp, EmpApp and BackendApp
app.register_blueprint(backendapp)
app.register_blueprint(adminapp,url_prefix='/admin')
app.register_blueprint(empapp,url_prefix='/emp')


# Page not found error handling
app.register_error_handler(404, page_not_found)


if __name__ == '__main__':
    app.run(debug = True)