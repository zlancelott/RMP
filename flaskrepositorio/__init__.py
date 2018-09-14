from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)


app.config['SECRET_KEY'] = '704f06afe4b162197fbeb4e1fc2dd9d1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/banco-rmd'
app.config['UPLOAD_FOLDER'] = './flaskrepositorio/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'home'

from flaskrepositorio import routes
