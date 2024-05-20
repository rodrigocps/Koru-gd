from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from .config import Config
# import app.database as config_db

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app import copy_empresas, models, routes, config_admin

with app.app_context():
    upgrade()

# from app import routes

# buildDb()
