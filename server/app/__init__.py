from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mimir-database.db'
app.config['JWT_SECRET_KEY'] = 'chn0531jea0412'

db = SQLAlchemy(app)
jwt = JWTManager(app)

from app import models

try:
    from app.routes import register_routes
    register_routes(app)
except ImportError:
    pass