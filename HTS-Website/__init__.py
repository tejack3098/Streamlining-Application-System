from flask import Flask, render_template, request,session, redirect, url_for, jsonify
import requests, json, base64, pymongo
from flask_cors import CORS


from routes.backend_routes import backend
from routes.admin_routes import adminapp
from routes.emp_routes import empapp


app = Flask(__name__)

CORS(app)
    
app.secret_key="abcdffgdefgac"

app.register_blueprint(backend)
app.register_blueprint(adminapp)
app.register_blueprint(empapp)


if __name__ == '__main__':
    app.run(debug = True)