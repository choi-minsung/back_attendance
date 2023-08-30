import os

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# = os.path.dirname(__file__)

class Config:
	SECRET_KEY = os.getenv('SECRET_KEY', 'ngle_api_tongchun')
	DEBUG = False

db = {
	'user' : 'KUINFOSadmin',
	'password' : 'alstjd123',
	'host' : 'localhost',
	'port' : 3306,
	'database' : 'User_DB'
}

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    # Swagger
    RESTX_MASK_SWAGGER = False



class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:alstjd123@localhost:3306/User_DB?charset=utf8".format(
        os.path.join(BASE_DIR, 'project.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:alstjd123@localhost:3306/User_DB?charset=utf8".format(
        os.path.join(BASE_DIR, 'project.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
