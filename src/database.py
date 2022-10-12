import os
import pymongo


class Mongo:
    def __init__(self, mongo_uri: str = None, iscommited: bool = True, reference_fileStore=None):
        if mongo_uri is None:
            self.mongo_uri = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017")
            # "mongodb://database/pythonmongodb"

    def connect(self):
        try:
            self.client = pymongo.MongoClient(self.mongo_uri)
        except:
            print("FAIL TO CONECT {self.mongo_uri}")
