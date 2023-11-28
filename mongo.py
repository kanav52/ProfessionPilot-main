import pymongo
# from bson.objectid import ObjectId
# from tabulate import tabulate


class MongoDBHelper:
    def __init__(self, collection=''):
        uri = "mongodb+srv://root:root@cluster0.vr3jyff.mongodb.net/?retryWrites=true&w=majority"
        client = pymongo.MongoClient(uri)
        self.db = client['Finalproject']
        self.collection = self.db[collection]
        print("MongoDB Connected...")

    def insert(self, document):
        result = self.collection.insert_one(document)
        print("Document inserted...", result)
        return result

    def delete(self, query):
        result = self.collection.delete_one(query)
        print("Document deleted...", result)

    def fetch(self, query=""):
        # documents = self.collection.find(query)
        # for document in documents:
        # print(document)
        # print(tabulate(documents, headers="keys", tablefmt="grid"))
        documents = self.collection.find(query)
        return list(documents)

    def update(self, document, query):
        update_query = {'$set': document}
        result = self.collection.update_one(query, update_query)
        print("Updated document...", result.modified_count)


