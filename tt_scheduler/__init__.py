from flask import Flask 
# from flask_sqlalchemy import SQLAlchemy
#from flask_bcrypt import Bcrypt 
# from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '842266388f2c6e4afc87a51854826973'#needs to be hidden during production
# login_manager = LoginManager(app)

from tt_scheduler import routes