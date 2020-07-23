from flask import Flask, render_template, request,session, redirect, url_for, jsonify
import requests, json, base64, pymongo
from flask_cors import CORS


from _backend_routes import backendapp
from _admin import adminapp
from _emp import empapp


app = Flask(__name__,static_folder='_static') # static_folder=None

CORS(app)
    
app.secret_key="abcdffgdefgac"

app.register_blueprint(backendapp)
app.register_blueprint(adminapp,url_prefix='/admin')
app.register_blueprint(empapp,url_prefix='/emp')


if __name__ == '__main__':
    app.run(debug = True)