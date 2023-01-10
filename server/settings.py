from os.path import join, dirname
from dotenv import load_dotenv
import os

dotenv_path = '.env'
load_dotenv(dotenv_path)


DATABASE_URI = {
    'user': "admin",
    'password': "Opcito123",
    'host': "meetingroomdb.cg08rmunlrsf.ap-south-1.rds.amazonaws.com",
    'database': "meeting_room",
}

# print(DATABASE_URI)
