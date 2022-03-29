#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      echo "Waiting for postgres $SQL_HOST..."
      sleep 1
    done

    echo "PostgreSQL started"
fi

if [ "$MODE" = "develop" ]
then
    mkdir ./logger
    sleep 1
    echo "Creating the database tables..."
    echo "Filling tables with ini data..."
    echo "Tables created and filled."
    python /usr/src/app/main.py fill
fi

if [ "$MODE" = "prod" ]
then
    sleep 1
    echo "Loading the database tables..."
    python /usr/src/app/main.py
fi



exec "$@"