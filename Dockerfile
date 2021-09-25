FROM python:3.7-alpine AS build-image

LABEL maintainer="nguyenkhacthanh244@gmail.com" version="1.0"

WORKDIR /app

ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

RUN apk update --no-cache && \
    apk add --no-cache gcc g++ musl-dev \
    libffi-dev openssl-dev make python3-dev jpeg-dev zlib-dev

ADD requirements.txt .

RUN python -mvenv env &&\
    source env/bin/activate && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

FROM python:3.7-alpine

WORKDIR /app

COPY --from=build-image /app/env ./env

ADD . .

RUN apk add python3-dev jpeg-dev zlib-dev

EXPOSE 5000

ENTRYPOINT env/bin/gunicorn -c gunicorn.config.py wsgi:main

CMD /bin/sh
