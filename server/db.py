from os import environ
import mysql.connector
from .settings import DATABASE_URI



def connect_db():
    return mysql.connector.connect(**DATABASE_URI)

# #.env
# DATABASE_HOST = "localhost"
# DATABASE_USER = "shubham"
# DATABASE_PASSWORD = ""
# DATABASE_NAME  = "meeting_room"


