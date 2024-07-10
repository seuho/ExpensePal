from pymongo import MongoClient
from config import ATLAS_URL
ATLAS_URI = ATLAS_URL
DB_NAME = 'ExpensePal'

class AtlasClient:
    def __init__(self, atlas_uri, dbname):
        self.mongodb_client = MongoClient(atlas_uri)
        self.database = self.mongodb_client[dbname]

    def get_collection(self, collection_name):
        collection = self.database[collection_name]
        return collection

    def ping(self):
        self.mongodb_client.admin.command('ping')

atlas_client = AtlasClient(ATLAS_URI, DB_NAME)