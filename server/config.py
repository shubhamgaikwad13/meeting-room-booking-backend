
class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_HOST = "127.0.0.1"
    DATABASE_USER = "shubham"
    DATABASE_PASSWORD = "Opcito@123"
    DATABASE_NAME = "meeting_room"
    DATABASE_URI = {
        'user': DATABASE_USER,
        'password': DATABASE_PASSWORD,
        'host': DATABASE_HOST,
        'database': DATABASE_NAME,
    }


class TestingConfig(Config):
    TESTING = True
