import os

from flask import Flask
from flask_pymongo import PyMongo

from flaskr.words.view import words_blueprint

pymongo = PyMongo()

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.logger.info("Flask app created")
    app.config["MONGO_URI"] = \
        f'mongodb://{os.environ["MONGO_INITDB_ROOT_USERNAME"]}:{os.environ["MONGO_INITDB_ROOT_PASSWORD"]}@' \
        f'{os.environ["MONGO_HOST"]}:{os.environ["MONGO_PORT"]}/{os.environ["MONGO_DATABASE"]}?authSource=admin'
    pymongo.init_app(app)

    app.register_blueprint(words_blueprint)

    return app