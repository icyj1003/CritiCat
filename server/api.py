import json
from typing import Union

from bson.json_util import dumps
from fastapi import FastAPI
from pymongo import MongoClient

# SETTINGS
MONGO_CONNECT_STRING = "mongodb+srv://noticy:76BZJDtw6KtzZn1W@cluster0.mlaq4tt.mongodb.net/?retryWrites=true&w=majority"


app = FastAPI()
client = MongoClient(MONGO_CONNECT_STRING)


@app.get("/")
def read_root():
    db = client["CritiCat"]
    coll = db["raw"]
    cursor = coll.find({})
    return json.loads(dumps(cursor))