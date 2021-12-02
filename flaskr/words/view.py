from flask import Blueprint, request, current_app, jsonify, make_response
from flask_restx import Api, Resource, fields, marshal_with
from mongoengine import NotUniqueError, FieldDoesNotExist

from flaskr.words.model import Word


words_blueprint = Blueprint('words', __name__)

api = Api(words_blueprint,
          version="1.0",
          title="Plytix Words REST API",
          description="A Plytix REST API"
          )

word_model = api.model('Word', {'word': fields.String, 'position': fields.Integer})
word_patch_model = api.model('WordPatch', {'position': fields.Integer})

@words_blueprint.app_errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@words_blueprint.app_errorhandler(405)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@words_blueprint.app_errorhandler(AssertionError)
def resource_not_found(e):
    return jsonify(error=f"Request body error"), 400


@words_blueprint.app_errorhandler(NotUniqueError)
def resource_not_found(e):
    return jsonify(error=f"Duplicate key error."), 400


@words_blueprint.app_errorhandler(FieldDoesNotExist)
def resource_not_found(e):
    return jsonify(error=f"Request body error."), 400


@api.route('/words')
class WordsPath(Resource):

    @api.response(201, 'Success')
    @api.response(400, 'Validation Error')
    @api.doc(body=word_model)
    def post(self):
        raw_word = request.get_json()
        word = Word(**raw_word).save()

        return make_response(word.to_json(), 201)

    @api.response(200, 'Success')
    def get(self):
        items = Word.objects.order_by("position", "-id")
        current_app.logger.info(items)
        data = [item.word for item in items]
        return make_response(jsonify({"data": data}), 200)


@api.route('/words/<word>')
class WordPath(Resource):

    @api.response(200, 'Success')
    @api.response(404, 'Not found')
    @api.doc(params={'word': 'A existing word listed by GET /words '},
             body=word_patch_model)
    def patch(self, word):
        Word.objects.get_or_404(word=word)

        raw_word = request.get_json()

        assert len(raw_word) == 1
        raw_word['word'] = word
        new_word = Word(**raw_word)

        # In order to have a new _id we need to delete and insert again, that will
        # maintain timestamped order based on _id
        Word.objects.get(word=word).delete()
        new_word.save()
        return make_response(new_word.to_json(), 200)

    @api.response(200, 'Success')
    @api.response(404, 'Not found')
    @api.doc(params={'word': 'A existing word listed by GET /words '})
    def delete(self, word):
        Word.objects.get_or_404(word=word)

        Word.objects.get(word=word).delete()
        return '', 204


@api.route('/words/<word>/anagrams')
class AnagramsPath(Resource):

    @api.doc(params={'word': 'A existing word listed by GET /words '})
    def get(self, word):
        items = Word.objects(__raw__={"$expr": {"$eq": [{"$strLenCP": "$word"},  len(word)]}}).order_by("position", "-id")

        sorted_word = sorted(word)
        data = [item['word'] for item in items if sorted(item['word']) == sorted_word]
        return make_response(jsonify({"data": data}), 200)
