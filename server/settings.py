from os.path import join, dirname
from dotenv import load_dotenv
import os

dotenv_path = '.env'
load_dotenv(dotenv_path)


DATABASE_URI = {
    'user': os.environ.get("DATABASE_USER"),
    'password': os.environ.get("DATABASE_PASSWORD"),
    'host': os.environ.get("DATABASE_HOST"),
    'database': os.environ.get("DATABASE_NAME"),
}

# print(DATABASE_URI)
