from sqlite3 import connect
import os

if os.getenv('DATABASE_URL'):
        DATABASE_PATH = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
else:
    DATABASE_PATH = "banco.db"
