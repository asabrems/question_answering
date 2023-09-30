class Config(object):
    DEBUG = False
    TESTING = False
    ELASTICSEARCH_URL = 'http://localhost:9200'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False
