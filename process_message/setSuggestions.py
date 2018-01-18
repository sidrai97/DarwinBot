from argsLoader import loadCmdArgs
import json, mongoCURD, symptomChecker

userid=str(loadCmdArgs(1))
suggestionSelected=str(loadCmdArgs(2)).split()
temp=[]
for t in suggestionSelected:
    temp.append({'id': t, 'initial': True, 'choice_id': 'present'})
payload=mongoCURD.getSymptomPayload(userid)
payload["symptoms_payload"]["evidence"]+=temp
symptomChecker.diagnosisHandler(userid,payload)