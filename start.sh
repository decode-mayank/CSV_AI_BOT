#!/bin/bash

cd flask-ai && flask db init

cd flask-ai && flask db migrate -m "Initial migration."

cd flask-ai && flask db upgrade

cd flask-ai && flask run