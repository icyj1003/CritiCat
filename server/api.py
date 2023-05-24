import json
from typing import Union

from bson.json_util import dumps
from fastapi import FastAPI
from pymongo import MongoClient

# SETTINGS
MONGO_CONNECT_STRING = "mongodb://mongo:27017"


app = FastAPI()
client = MongoClient(MONGO_CONNECT_STRING)


@app.get("/")
def read_root():
    db = client["CritiCat"]
    coll = db["raw"]
    cursor = coll.find({})
    return json.loads(dumps(cursor))