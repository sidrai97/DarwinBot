def getDbConnection():
    from pymongo import MongoClient
    client=MongoClient('localhost', 27017)
    return client

def insertUserDataFromFb(document):
    client=getDbConnection()
    db=client.darwin
    db.users.insert(document)
    client.close()
    return

def setDetails(userid,dob,weight,height,location,injury):
    client=getDbConnection()
    db=client.darwin
    result=db.users.update_one({'_id': userid}, {'$set': {'dob': dob,'weight':weight,'height':height,'location':location,'injury':injury}})
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

def getAgeGender(userid):
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

def getDetails(userid):
    client=getDbConnection()
    db=client.darwin
    result=db.users.find({"$and":[{'_id':userid},{'dob':{"$exists":True}}]},{"gender":1,"dob":1,"weight":1,"height":1,"location":1,"injury":1,"_id":0})
    client.close()
    if result.count() > 0:
        return result[0]
    return {}

def setSymptomPayload(userid,payload):
    if "symptoms_payload" in payload:
        payload = payload["symptoms_payload"]
    client=getDbConnection()
    db=client.darwin
    result=db.users.update_one({'_id': userid}, {'$set': {'symptoms_payload': payload}})
    client.close()
    return

def getSymptomPayload(userid):
    client=getDbConnection()
    db=client.darwin
    result=db.users.find({'_id': userid}, {'symptoms_payload':1,'_id':0})
    client.close()
    if result.count() > 0:
        return result[0]
    return {}

def getQuestionsCount(userid):
    client=getDbConnection()
    db=client.darwin
    result=db.users.find({'_id': userid}, {'questions_count':1,'_id':0})
    client.close()
    if result.count() > 0:
        return result[0]
    return {}

def setQuestionsCount(userid,count):
    client=getDbConnection()
    db=client.darwin
    result=db.users.update_one({'_id': userid}, {'$set': {'questions_count': count}})
    client.close()
    return
#def getExercisesQuery(level=[ 'beginner', 'intermediate', 'expert' ],muscle=[ 'shoulders' ],etype=[ 'strength', 'powerlifting' ],equipment=[]):
def getExercisesQuery(level,muscle,etype,equipment):
    client=getDbConnection()
    db=client.darwin
    query=[]
    if len(level) > 0:
        query.append({'level':{'$in':level}})
    if len(muscle) > 0:
        query.append({'muscle':{'$in':muscle}})
    if len(etype) > 0:
        query.append({'type':{'$in':etype}})
    if len(equipment) > 0:
        query.append({'equipment':{'$in':equipment}})
    result=db.exercise_encyclopedia.find({ '$and':query}, {'name':1,'_id':1,'level':1,'muscle':1,'type':1,'equipment':1,'right_img_url':1})
    #result=db.exercise_encyclopedia.find({'level':{'$in':['beginner']}, 'muscle':{'$in':['chest']},'type':{'$in':['strength'], 'equipment':{'$in':['bodyonly']} }, {'name':1,'_id':1,'level':1,'muscle':1,'type':1,'equipment':1})
    client.close()
    result=list(result)
    for r in result:
        r["_id"]=str(r["_id"])
    if len(result) > 0:
        return list(result)
    return []

def getExercisesDetails(eid):
    from bson.objectid import ObjectId
    client=getDbConnection()
    db=client.darwin
    result=db.exercise_encyclopedia.find({'_id':ObjectId(eid)}, {'_id':0})
    client.close()
    result=list(result)
    if len(result) > 0:
        return result
    return []

def storeWorkoutLog(userid,data):
    client=getDbConnection()
    db=client.darwin
    result=db.users.update({'_id': userid}, {'$push': {'workoutLog': data} })
    client.close()
    return