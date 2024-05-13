from flask import Flask
from app.create_database import buildDb

app = Flask(__name__)

app.config['SECRET_KEY'] = '123456789'

from app import routes

buildDb()
