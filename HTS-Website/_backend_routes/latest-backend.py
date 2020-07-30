from flask import Flask,render_template,request,jsonify
from datetime import datetime
from datetime import timedelta
import calendar
import pickle

import base64
from flask_cors import CORS
import pymongo
from barcode import generate
from barcode.writer import ImageWriter

app = Flask(__name__)
CORS(app)
iwriter = ImageWriter()

if __name__ == "__main__":
    app.run(debug=True,port=5000)