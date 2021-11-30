from flask import Blueprint, request, current_app, jsonify
from flask_pymongo import ASCENDING, DESCENDING
from flask_pymongo.wrappers import Collection
from pydantic import ValidationError
from pymongo.errors import DuplicateKeyError

import flaskr
from flaskr.words.model import Word

words_blueprint = Blueprint('words', __name__)
words_collection: Collection = None


@words_blueprint.app_errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@words_blueprint.app_errorhandler(405)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@words_blueprint.app_errorhandler(ValidationError)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@words_blueprint.app_errorhandler(AssertionError)
def resource_not_found(e):
    return jsonify(error=f"Request body error"), 400


@words_blueprint.app_errorhandler(DuplicateKeyError)
def resource_not_found(e):
    return jsonify(error=f"Duplicate key error."), 400


@words_blueprint.before_app_first_request
def init_my_blueprint():
    global words_collection
    words_collection = flaskr.pymongo.db.words
    current_app.logger.info('First app request')
    words_collection.create_index([("name", ASCENDING), ("_id", DESCENDING)], unique=True)


@words_blueprint.route('/words', methods=['GET', 'POST'])
def words_path():

    if request.method == 'POST':
        raw_word = request.get_json()
        current_app.logger.info(raw_word)
        word = Word(**raw_word)

        insert_result = words_collection.insert_one(word.to_bson())
        # TODO db error handling
        return word.to_json()

    elif request.method == 'GET':
        items = words_collection.find({}).sort([("position", ASCENDING), ("_id", DESCENDING)])
        data = [item['word'] for item in items]
        return jsonify({"data": data})


@words_blueprint.route('/words/<word>', methods=['PATCH', 'DELETE'])
def word_path(word):
    words_collection.find_one_or_404({"word": word})

    if request.method == 'PATCH':
        raw_word = request.get_json()
        assert len(raw_word) == 1
        raw_word['word'] = word
        new_word = Word(**raw_word)

        words_collection.delete_one({"word": word})
        words_collection.insert_one(new_word.to_bson())
        return new_word.to_json()

    elif request.method == 'DELETE':
        words_collection.delete_one({"word": word})
        return '', 204


@words_blueprint.route('/words/<word>/anagrams', methods=['GET'])
def anagrams_path(word):
    items = words_collection.find({"$expr": {"$eq": [{"$strLenCP": "$word"},  len(word)]}}).sort([("position", ASCENDING), ("_id", DESCENDING)])
    sorted_word = sorted(word)
    data = [item['word'] for item in items if sorted(item['word']) == sorted_word]
    return jsonify({"data": data})
