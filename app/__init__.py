import logging
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix
from settings import config

db = SQLAlchemy()

def create_app(cnf=None):
    '''
        Create skeleton application...
    '''
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    if cnf:
        app.config.from_object(config[cnf])
        config[cnf].init_app(app)

    db.init_app(app)
    if app.config['APP_MODE'] == 'production':
        log = logging.getLogger('wekzeug')
        log.setLevel(logging.INFO)
        loghandler = logging.StreamHandler(sys.stdout)
        loghandler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - \
                                      %(levelname)s - %(message)s')
        loghandler.setFormatter(formatter)
        app.logger.addHandler(loghandler)

    from .bootfiles import bp as bootfiles_blueprint
    app.register_blueprint(bootfiles_blueprint, url_prefix='/bootfiles')

    from .bootconf import bp as bootconf_blueprint
    app.register_blueprint(bootconf_blueprint, url_prefix='/bootconf')

    return app
