import json
from pydantic import BaseModel


class Word(BaseModel):
    word: str
    position: int

    def to_json(self):
        return json.dump({"name": self.name, "position": self.position})

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data.get("_id") is None:
            data.pop("_id", None)
        return data