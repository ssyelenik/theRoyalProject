import flask
import flask_sqlalchemy
import flask_migrate
import flask_login
import flask_mail
import os

db=flask_sqlalchemy.SQLAlchemy()
migrate=flask_migrate.Migrate()
login_mgr=flask_login.LoginManager()
mail_mgr=flask_mail.Mail()

def create_app(default_env="development"):
    from config import config

    from .views import main_blueprint
    from .auth import auth_blueprint
    from . import models

    app=flask.Flask(__name__)

    env = os.environ.get("FLASK_ENV", default_env)
    app.config.from_object(config[env])

    db.init_app(app)
    login_mgr.init_app(app)
    migrate.init_app(app,db)
    mail_mgr.init_app(app)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint,url_prefix="/auth")

    return app