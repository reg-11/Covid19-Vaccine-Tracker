
# from psycopg2 import connect
from flask import Flask, request, jsonify, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
import os
from datetime import date

from marshmallow import Schema, fields, ValidationError, pre_load

# #Init db
db = SQLAlchemy()

def create_app():

	# Init app
	app = Flask(__name__)                 
	app.secret_key = "Secret Key"

	# Database
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://kumlmkrpwvtffp:34ffa0b9a4e5d85ba1679d979c2ff64938edc35e2f58f18dcf68f0b76610bb97@ec2-54-157-66-140.compute-1.amazonaws.com/daj0298ke4iu1b'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	# #Init db
	# db = SQLAlchemy(app)

	# # Init ma
	# ma = Marshmallow(app)

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	# Run Server
	return app

