from flasgger import Swagger

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from api.route.home import home_api
from config import Config

import os

def create_app():
    newApp = Flask(__name__)

    newApp.config.from_object(Config)
    newApp.config['SWAGGER'] = {
        'title': 'Flask API Starter Kit',
    }
    newApp.config.from_object(os.environ['APP_SETTINGS'])
    newApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    swagger = Swagger(newApp)

    newApp.register_blueprint(home_api, url_prefix='/api')

    return newApp


app = create_app()
db = SQLAlchemy(app)
login = LoginManager(app)
from api.model import user

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
