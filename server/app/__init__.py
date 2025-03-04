from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mimir-database.db'
db = SQLAlchemy(app)

from app import models
from app.routes import register_routes
register_routes(app)
