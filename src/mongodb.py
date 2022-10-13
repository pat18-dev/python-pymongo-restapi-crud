from os import getenv
from sys import stderr
import traceback
import pymongo


class Mongo:
    def __init__(self, collection: str, mongo_uri: str = None, db: str = None):
        print("INIT", file=stderr)
        print("-" * 60, file=stderr)
        if mongo_uri is None:
            self.mongo_uri = getenv("MONGO_URI", "mongodb://127.0.0.1:27017/")
            # "mongodb://127.0.0.1:27017/"
            # "mongodb://database/pythonmongodb"
        if db is None:
            self.db = getenv("DATABASE", "db")
        print(self.mongo_uri, file=stderr)
        print(self.db, file=stderr)
        try:
            self.client = pymongo.MongoClient(self.mongo_uri)
            self.db = self.client[db]
            self.collection = db[collection]
        except Exception as err:
            print(type(err), file=stderr)
            print(str(err), file=stderr)
            print(err.__class__.__name__, file=stderr)
            traceback.print_exc()
            print("-" * 60, file=stderr)