#!venv/bin/python

import os
from app import create_app


app = create_app(os.environ.get('FLASK_APP_MODE'))


if __name__ == '__main__':
    app.run()
