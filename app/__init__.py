from flask import Flask, session

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789'
from app import routes
