from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask.ext.mongoalchemy import MongoAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '4b5402378ffe97929b29f1b25a178254'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# app.config['MONGOALCHEMY_DATABASE'] = 'library'

db = SQLAlchemy(app)
# mongo = MongoAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'

from SIG_EmDis import routes