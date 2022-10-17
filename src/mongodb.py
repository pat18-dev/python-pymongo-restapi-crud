from os import getenv
from sys import stderr
import traceback
import pymongo

def connect(collection: str, mongo_uri: str = None, db: str = None):
    print("INIT", file=stderr)
    print("-" * 60, file=stderr)
    if mongo_uri is None:
        mongo_uri = getenv("MONGO_URI", "mongodb://127.0.0.1:27017/")
        # "mongodb://127.0.0.1:27017/"
        # "mongodb://database/pythonmongodb"
    if db is None:
        db = getenv("DATABASE", "db")
    try:
        client = pymongo.MongoClient(mongo_uri)
        print("---DB", file=stderr)
        print(client.getDatabaseNames(), file=stderr)
        db = client[db]
        return db[collection]
    except Exception as err:
        print(type(err), file=stderr)
        print(str(err), file=stderr)
        print(err.__class__.__name__, file=stderr)
        traceback.print_exc()
        print("-" * 60, file=stderr)