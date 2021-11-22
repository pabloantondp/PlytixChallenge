from flask import Blueprint, request, current_app
import flaskr
from flaskr.words.model import Word
words_blueprint = Blueprint('words', __name__)


@words_blueprint.route('/words', methods=['GET', 'POST'])
def words():

    if request.method == 'POST':
        raw_word = request.get_json()
        current_app.logger.info(raw_word)
        word = Word(**raw_word)
        insert_result = flaskr.pymongo.words.insert_one(word.to_bson())

        return {}
    elif request.method == 'GET':
        items = flaskr.pymongo.words.find({})

        return "Get"

