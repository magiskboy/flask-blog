web: gunicorn --worker-class=gevent wsgi:main
upgrade: FLASK_ENV=production FLASK_APP=wsgi:main flask db upgrade
