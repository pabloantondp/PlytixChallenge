import os

from flask import Flask

from flaskr.database.db import initialize_db
from flaskr.words.view import words_blueprint


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.logger.info("Flask app created")
    app.config['MONGODB_SETTINGS'] = {
        'connect': True,
        'host': f'mongodb://{os.environ["MONGO_INITDB_ROOT_USERNAME"]}:{os.environ["MONGO_INITDB_ROOT_PASSWORD"]}@'
                f'{os.environ["MONGO_HOST"]}:{os.environ["MONGO_PORT"]}/{os.environ["MONGO_DATABASE"]}?authSource=admin'}
    initialize_db(app)

    app.register_blueprint(words_blueprint)

    return app
