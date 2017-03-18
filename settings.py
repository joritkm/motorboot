import os

"""
Settings for motorboot app
===========================================
"""

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    APP_MODE = os.environ.get('FLASK_APP_MODE',
                              'default')
    SECRET_KEY= os.environ.get('FLASK_APP_KEY',
                               'default')
    LOGPATH = os.environ.get('FLASK_APP_LOGDIR',
                             'default')
    if LOGPATH == 'default':
        LOGPATH = os.path.join(basedir,'logs')
    else:
        LOGPATH = os.path.abspath(LOGPATH)
        if not os.path.exists(LOGPATH):
            os.mkdir(LOGPATH)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    BOOTFILES = os.path.abspath(os.environ.get('BOOTFILES'))
    if not os.path.exists(BOOTFILES):
        os.mkdir(BOOTFILES)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ \
            os.path.join(basedir,'{}'.format('mb_dev.sqlite'))


class ProductionConfig(Config):
    DEBUG=False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ \
            os.path.join(basedir,'{}'.format('mb_prod.sqlite'))

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ \
            os.path.join(basedir,'{}'.format('mb_test.sqlite'))
    DEBUG=True
    TESTING=True
    FLASK_COVERAGE = 1


config = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,

        'default': DevelopmentConfig
        }
