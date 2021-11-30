import json

from flaskr.words.model import Word


def test_api_get_empty(empty_db_client):
    assert empty_db_client is not None
    rv = empty_db_client.get('/words')
    assert rv.data is not None


def test_api_malformed_post(empty_db_client):
    response = empty_db_client.post(
        '/words',
        data=json.dumps({"word": "palabra"}),
        content_type='application/json',
    )

    assert response.status_code == 404


def test_api_count_empty(empty_db_client):
    assert empty_db_client is not None
    response = empty_db_client.get('/words')
    assert response is not None
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert len(data['data']) == 0


def test_api_get(initialized_db_client):
    response = initialized_db_client.get('/words')

    json_data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    data = json_data['data']
    assert len(data) == 5
    assert data[0] == "cosa"
    assert data[1] == "caso"
    assert data[2] == "paco"
    assert data[3] == "pepe"
    assert data[4] == "Malaga"


def test_api_post(initialized_db_client):
    test_word = Word(word="calle", position=3)
    response = initialized_db_client.post(
        '/words',
        data=test_word.to_json(),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert len(data) == 2
    assert data['word'] == "calle"
    assert data['position'] == 3

    response = initialized_db_client.get('/words')

    json_data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    data = json_data['data']
    assert len(data) == 6
    assert data[0] == "cosa"
    assert data[1] == "caso"
    assert data[2] == "calle"
    assert data[3] == "paco"
    assert data[4] == "pepe"
    assert data[5] == "Malaga"


def test_api_patch(initialized_db_client):
    test_word = Word(word="calle", position=3)
    patch_data = {"position": 5}
    response = initialized_db_client.post(
        '/words',
        data=test_word.to_json(),
        content_type='application/json',
    )
    assert response.status_code == 200

    response = initialized_db_client.patch('/words/calle',
                                          data=json.dumps({"position": 5}),
                                          content_type='application/json')
    json_data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert json_data['word'] == "calle"
    assert json_data['position'] == 5


def test_api_delete_error(empty_db_client):
    response = empty_db_client.delete('/words/what')
    assert response.status_code == 404


def test_api_delete(initialized_db_client):
    response = initialized_db_client.get('/words')

    json_data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    data = json_data['data']
    assert len(data) == 5
    assert 'cosa' in data

    response = initialized_db_client.delete('/words/cosa')
    assert response.status_code == 204

    response = initialized_db_client.get('/words')

    json_data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    data = json_data['data']
    assert len(data) == 4
    assert 'cosa' not in data


def test_api_delete(initialized_db_client):
    response = initialized_db_client.get('/words/asco/anagrams')

    json_data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    data = json_data['data']
    assert len(data) == 2
    assert data[0] == 'cosa'
    assert data[1] == 'caso'