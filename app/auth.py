from flask_httpauth import HTTPTokenAuth
from flask import g
from settings import Config
import yaml

auth = HTTPTokenAuth(scheme='Token')

with open(Config.SECRETSFILE) as secrets:
    secrets_dict = yaml.load(secrets)


@auth.verify_token
def verify_token(token):
    if token in secrets_dict:
        g.current_user = secrets_dict[token]
        return True
    else:
        return False
