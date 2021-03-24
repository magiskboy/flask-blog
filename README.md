# Simple blog application

### Notice before run?

Application needs some environments:
- GOOGLE_CLIENT_ID
- GOOGLE_CLIENT_SECRET
- FACEBOOK_CLIENT_ID
- FACEBOOK_CLIENT_SECRET

and need to export FLASK_ENV=development for development env

### Run with docker-compose

Consider docker-compose.yml before execute following commands

```sh
$ docker-compose up -d
```


### Run without docker-compose

```sh
$ virtualenv env
$ source env/bin/activate
$ FLASK_ENV=development FLASK_APP=wsgi:app <google and facebook key> flask run
```
