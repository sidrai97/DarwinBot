import infermedica_api
import mongoCURD

def makeApiObj(app_id,app_key):
    return infermedica_api.API(app_id=app_id, app_key=app_key)

def parse(api,msg):
    return api.parse(msg, include_tokens=True)

def diagnosis(userid,api,mentions,raw=False):
    if raw:
        sex=mentions['symptoms']['sex']
        age=mentions['symptoms']['age']
        evidence=mentions['symptoms']['evidence']
        request=infermedica_api.Diagnosis(sex=sex, age=age)
        for obj in evidence:
            request.add_symptom(obj['id'], obj['choice_id'])
    else:
        #get gender and age from db
        tup=mongoCURD.getAgeDob(userid)
        age=tup[0]
        gender=tup[1]
        request=infermedica_api.Diagnosis(sex=gender, age=age)
        #find symptoms/risk factor in mentions
        for obj in mentions:
            if obj['type'] == 'symptom':
                request.add_symptom(obj['id'], obj['choice_id'])
            elif obj['type'] == 'risk_factor':
                request.add_risk_factor(obj['id'], obj['choice_id'])
    
    #send diagnosis request
    response=api.diagnosis(request)
    return response
    
