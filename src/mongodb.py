from os import getenv
from sys import stderr
import traceback
from pymongo import MongoClient


def connect(collection: str = None, mongo_uri: str = None, db: str = None):
    print("INIT", file=stderr)
    print("-" * 60, file=stderr)
    if mongo_uri is None:
        mongo_uri = getenv("MONGO_URI", "mongodb://database/pythonmongodb")
        # "mongodb://127.0.0.1:27017/"
        # "mongodb://database/pythonmongodb"
    if db is None:
        db = getenv("DATABASE", "db")
    try:
        client = MongoClient(mongo_uri)
        print("---DB", file=stderr)
        print(client.list_database_names(), file=stderr)
        if collection is None:
            return None
        else:
            db = client[db]
            print(db.collection_names(), file=stderr)
            return db[collection]
    except Exception as err:
        print(type(err), file=stderr)
        print(str(err), file=stderr)
        print(err.__class__.__name__, file=stderr)
        traceback.print_exc()
        print("-" * 60, file=stderr)
