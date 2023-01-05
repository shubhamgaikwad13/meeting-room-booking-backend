from .settings import DATABASE_URI


class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = DATABASE_URI


class TestingConfig(Config):
    TESTING = True
