from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:komojini@localhost:5432/johnnys_shop'
app.config['SECRET_KEY'] = '7cbebf954748b1a7f55c'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# login_manager.login_view = 'login_page'
# login_manager.login_message_category = 'info'
from shop import routes



