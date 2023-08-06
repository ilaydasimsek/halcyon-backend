FROM python:3.9.16-slim

ENV PYTHONUNBUFFERED 1
ENV ENVIRONMENT dev

RUN apt-get update && \
    # required for building psycopg2
    # https://www.psycopg.org/articles/2018/02/08/psycopg-274-released/
    apt-get install -y libpq-dev && \
    apt-get clean


COPY requirements.txt /tmp/
COPY requirements-dev.txt /tmp/

WORKDIR /app

RUN pip install pip-tools && \
    pip-sync /tmp/requirements.txt /tmp/requirements-dev.txt

#ARG UID=1000
#ARG GID=1000
#RUN groupadd -g "${GID}" -r halcyon && \
#    useradd -m -g halcyon -r -u ${UID} halcyon
#
#COPY --chown=halcyon:halcyon . /app
#
#USER halcyon
