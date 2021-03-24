import os
from app import create_app

FLASK_ENV = os.getenv('FLASK_ENV')
app = create_app(FLASK_ENV)
