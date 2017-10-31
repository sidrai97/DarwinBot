def getDbConnection():
    from pymongo import MongoClient
    client=MongoClient('localhost', 27017)
    return client.darwin

def insertUserData(document):
    db=getDbConnection()
    db.users.insert(document)
    return

def updateDOB(userid,dob):
    db=getDbConnection()
    result=db.users.update_one({'_id': userid}, {'$set': {'dob': dob}})
    return

def checkDOBExists(userId):
    db=getDbConnection()
    result=db.users.find({"$and":[{'_id':userId},{'dob':{"$exists":True}}]})
    if result.count() > 0:
        return True
    return False