import os

from flask import Flask
from flask_pymongo import PyMongo

from flaskr.words.view import words_blueprint

pymongo = PyMongo()

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.logger.info("Flask app created")
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
    pymongo.init_app(app)

    app.register_blueprint(words_blueprint)

    return app