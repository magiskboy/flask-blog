web: gunicorn -c gunicorn.config.py wsgi:main
upgrade: FLASK_ENV=production FLASK_APP=wsgi:main flask db upgrade
