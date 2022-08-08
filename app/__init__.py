from flask import Flask
from flask_sqlalchemy import SQLAlchemy, inspect
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager
from .user import User
from .transaction import Transaction


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login = LoginManager(app)
login.init_app(app)
login.login_view = 'login'


migrate = Migrate(app, db)

from app import views, models

