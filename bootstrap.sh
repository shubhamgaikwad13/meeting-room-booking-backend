#!/bin/sh
export FLASK_APP=./server
export FLASK_ENV=development
export FLASK_DEBUG=1
flask run -p 5001

# flask-mysql = "*"
# mysql-connector-python = "*"
# python-dotenv = "*"
# flask-sqlalchemy = "*" -p 5001 -p 5001

# flask-mysql = "*"
# mysql-connector-python = "*"
# python-dotenv = "*"
# flask-sqlalchemy = "*"