import json
from flaskr.database.db import db


class Word(db.Document):
    word = db.StringField(required=True, unique=True)
    position = db.IntField(required=True, min_value=0)

    meta = {
        'indexes': [
            ('position', '-id')  # compound index
        ]
    }
    def to_json(self):
        return json.dumps({"word": self.word, "position": self.position})
