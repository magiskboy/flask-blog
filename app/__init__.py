from flask import Flask

from .security import login_manager
from .models import db
from .config import get_config
from .main import bp as main_bp
from .oauth2 import bp as oauth2_bp


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    login_manager.init_app(app)
    db.init_app(app)

    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(oauth2_bp, url_prefix='/oauth2')

    return app










































