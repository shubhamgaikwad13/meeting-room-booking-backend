from os import environ
import mysql.connector
from .settings import DATABASE_URI
from flask import g


def connect_db():
    if not hasattr(g, 'mysql_db'):
        g.mysql_db = mysql.connector.connect(**DATABASE_URI)
    return g.mysql_db

# #.env
# DATABASE_HOST = "localhost"
# DATABASE_USER = "shubham"
# DATABASE_PASSWORD = ""
# DATABASE_NAME  = "meeting_room"


