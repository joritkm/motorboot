import os

"""
Settings for motorboot app
===========================================
"""

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    APP_MODE = os.environ.get('FLASK_APP_MODE', 'default')

    SECRET_KEY= os.environ.get('MOTORBOOT_APPKEY', 'toomanysecrets')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')

    BOOTFILES = os.path.abspath(os.environ.get('BOOTFILES'))
    if not os.path.exists(BOOTFILES):
        os.mkdir(BOOTFILES)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG=True


class ProductionConfig(Config):
    DEBUG=False

class TestingConfig(Config):
    DEBUG=True
    TESTING=True
    FLASK_COVERAGE = 1


config = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,

        'default': DevelopmentConfig
        }
