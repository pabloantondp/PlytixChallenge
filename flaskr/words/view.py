from flask import Blueprint, request, current_app, jsonify
import flaskr
from flaskr.words.model import Word

words_blueprint = Blueprint('words', __name__)


@words_blueprint.route('/words', methods=['GET', 'POST'])
def words():

    if request.method == 'POST':
        raw_word = request.get_json()
        current_app.logger.info(raw_word)
        word = Word(**raw_word)
        insert_result = flaskr.pymongo.db.words.insert_one(word.to_bson())

        # TODO db error handling
        return word.to_json()

    elif request.method == 'GET':
        items = flaskr.pymongo.db.words.find({}).sort("position", 1)
        data = [item['word'] for item in list(items)]
        current_app.logger.info(data)
        return jsonify({"data": data})
