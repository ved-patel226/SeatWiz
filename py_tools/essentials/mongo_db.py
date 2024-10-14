from pymongo import MongoClient
try:
    from env_to_var import env_to_var
except:
    from .env_to_var import env_to_var

class MongoDBHandler:
    def __init__(self, uri=env_to_var("MONGO_URI"), db_name="SeatWiz"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def insert_one(self, collection_name, document):
        collection = self.db[collection_name]
        result = collection.insert_one(document)
        return result.inserted_id

    def find_one(self, collection_name, query):
        collection = self.db[collection_name]
        return collection.find_one(query)

    def find_many(self, collection_name, query):
        collection = self.db[collection_name]
        return list(collection.find(query))

    def update_one(self, collection_name, query, update):
        collection = self.db[collection_name]
        result = collection.update_one(query, {'$set': update})
        return result.modified_count

    def delete_one(self, collection_name, query):
        collection = self.db[collection_name]
        result = collection.delete_one(query)
        return result.deleted_count
    
    def close(self):
        self.client.close()

def main() -> None:
    mongo = MongoDBHandler()
    print(mongo.find_many("seating", {"username": "adfsa"}))

if __name__ == '__main__':
    main()