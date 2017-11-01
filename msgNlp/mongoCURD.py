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

def getAgeDob(userid):
    client=getDbConnection()
    db=client.darwin
    result=db.users.find({'_id':str(userid)},{'gender':1,'dob':1,'_id':0})
    dob=result[0]['dob']
    gender=result[0]['gender']
    age=ageCalc(dob)
    client.close()
    return (age,gender)

def ageCalc(dob):
    dob=dob.split('-')
    birthyear=int(dob[0])
    import datetime
    currentyear=datetime.date.today().year
    age=abs(birthyear-currentyear)
    return age