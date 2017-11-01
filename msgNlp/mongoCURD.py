def getDbConnection():
    from pymongo import MongoClient
    client=MongoClient('localhost', 27017)
    return client

def insertUserData(document):
    client=getDbConnection()
    db=client.darwin
    db.users.insert(document)
    client.close()
    return

def updateDOB(userid,dob):
    client=getDbConnection()
    db=client.darwin
    result=db.users.update_one({'_id': userid}, {'$set': {'dob': dob}})
    client.close()
    return

def checkDOBExists(userId):
    client=getDbConnection()
    db=client.darwin
    result=db.users.find({"$and":[{'_id':userId},{'dob':{"$exists":True}}]})
    client.close()
    if result.count() > 0:
        return True
    return False