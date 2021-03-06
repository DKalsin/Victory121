FROM python:3-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apk update \
  && apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev \
  && pip3 install -r requirements.txt \
  && apk --purge del .build-deps
COPY . /code/
