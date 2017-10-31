def insertUserData(document):
    from pymongo import MongoClient
    client=MongoClient('localhost', 27017)
    db=client.darwin
    db.users.insert(document)
    return