import random

import pytest

from flaskr import create_app
from flaskr.words.model import Word


@pytest.fixture
def empty_db_client():
    app = create_app()

    Word.objects.delete()
    return app.test_client()


@pytest.fixture
def initialized_db_client(empty_db_client):
    initial_items = [Word(word="cosa", position=1),
                     Word(word="caso", position=2),
                     Word(word="paco", position=3),
                     Word(word="pepe", position=4),
                     Word(word="Malaga", position=5)]
    random.shuffle(initial_items)
    for word in initial_items:
        word.save()

    return empty_db_client