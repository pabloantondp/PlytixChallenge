import random

import pytest

from flaskr import create_app, pymongo
from flaskr.words.model import Word


@pytest.fixture
def empty_db_client():
    app = create_app()

    pymongo.db.words.delete_many({})
    return app.test_client()


@pytest.fixture
def initialized_db_client(empty_db_client):
    initial_items = list([Word(word="cosa", position=1),
                     Word(word="caso", position=2),
                     Word(word="paco", position=3),
                     Word(word="pepe", position=4),
                     Word(word="Malaga", position=5)])
    random.shuffle(initial_items)
    for word in initial_items:
        response = empty_db_client.post(
            '/words',
            data=word.to_json(),
            content_type='application/json',
        )

        assert response.status_code == 200

    return empty_db_client