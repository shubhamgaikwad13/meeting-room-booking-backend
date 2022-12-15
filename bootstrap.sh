#!/bin/sh
export FLASK_APP=./server/app.py
export FLASK_ENV=development
export FLASK_DEBUG=1
flask run --port 5001