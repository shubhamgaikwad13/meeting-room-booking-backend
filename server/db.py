from os import environ
import mysql.connector
# from .settings import DATABASE_URI
from flask import g, current_app


def connect_db():
    # with current_app.app_context():
    #     print("db-config", current_app.config)
    if not hasattr(g, 'mysql_db'):
        g.mysql_db = mysql.connector.connect(
            **(current_app.config["DATABASE_URI"]))
    return g.mysql_db
