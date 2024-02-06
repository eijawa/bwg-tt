FROM python:3.12

WORKDIR /server

ARG POSTGRES__DBHOST
ENV POSTGRES__DBHOST=${POSTGRES__DBHOST}

COPY ./requirements.txt /server/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /server/requirements.txt

COPY ./environments /server/environments
COPY ./src /server/src

COPY ./alembic.ini /server/alembic.ini
COPY ./.alembic /server/.alembic

COPY ./entrypoint.sh /server/entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]