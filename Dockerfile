FROM python:3.7-alpine AS build-image

LABEL maintainer="nguyenkhacthanh244@gmail.com" version="1.0"

WORKDIR /app

ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

RUN apk update --no-cache && \
    apk add --no-cache gcc g++ musl-dev libffi-dev openssl-dev make

ADD requirements.txt .

RUN python -mvenv env &&\
    source env/bin/activate &&\
    pip install --no-cache-dir -r requirements.txt

FROM python:3.7-alpine

WORKDIR /app

COPY --from=build-image /app/env ./env

ADD . .

EXPOSE 5000

ENTRYPOINT env/bin/gunicorn -c gunicorn.config.py wsgi:app

CMD /bin/sh
