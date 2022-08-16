import pymongo

passd = "ckZpYU8HGpnc5i9i"
named = "CopySys"

client = pymongo.MongoClient("mongodb+srv://test:"+passd+"@cluster1.9glic.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.get_database(named)

class user():
    def findsession(collection, Owenr):
        collection = db[collection]
        session = {"Owenr":Owenr}
        data = collection.find(session)
        countsessions = collection.count_documents(session)
        return data, countsessions

    def findwords(collection, Owenr, target):
        collection = db[collection]
        words = {"Owenr":Owenr, "target":target}
        data = collection.find(words)
        countwords = collection.count_documents(words)
        return data, countwords