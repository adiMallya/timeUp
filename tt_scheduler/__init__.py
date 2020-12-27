from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager
# from flask_bootstrap import Bootstrap

from config import app_config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')


    # Bootstrap(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page"
    login_manager.login_view = "auth.login"
    with app.app_context():
        if db.engine.url.drivername == 'sqlite':
            migrate.init_app(app, db, compare_type=True, render_as_batch=True)
        else:
            migrate.init_app(app, db)


    from tt_scheduler import models

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    return app 
