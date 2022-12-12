from os import environ
import mysql.connector
from settings import DATABASE_URI



def connect_db():
    return mysql.connector.connect(**DATABASE_URI)

print(connect_db())