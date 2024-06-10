from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt



app: Flask = Flask(__name__)
app.config['SECRET_KEY'] = '5sfjshgfjkhsgf554654saffasjask'
app.config['SQLALCHEMY_DATABASE_URI']: str = 'sqlite:///car_repair.db'
db: SQLAlchemy = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

bcrypt = Bcrypt(app)

app.app_context().push()


# Important ! Keep this import at the end !
from car_repair_shop_project import routes
