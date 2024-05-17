import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '123456789'
    ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'database.db')

    # SQLALCHEMY_DATABASE_URI = "postgresql://korujobsdb_user:3mUWHnfdkmECfd7omsXnFcSptem0SJDQ@dpg-cp17shn79t8c73a3nkcg-a.oregon-postgres.render.com/korujobsdb"