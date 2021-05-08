"""
Flask app module
"""

from os import environ

from flask import Flask
from flask_mongoengine import MongoEngine

# TRM
TRM_USER_SERVICE_URL = 'https://trm-colombia.vercel.app/?date={}'

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'host': environ.get('MONGO_URI') or 'mongodb://127.0.0.1:27010/bankaccountservice'
}

db = MongoEngine()
db.init_app(app)
