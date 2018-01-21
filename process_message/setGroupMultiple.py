from argsLoader import loadCmdArgs
import json, mongoCURD, symptomChecker

userid=str(loadCmdArgs(1))
optionSelected=str(loadCmdArgs(2)).split()
temp=[]
for t in optionSelected:
    temp.append({'id': t, 'choice_id': 'present'})
payload=mongoCURD.getSymptomPayload(userid)
payload["symptoms_payload"]["evidence"]+=temp
symptomChecker.diagnosisHandler(userid,payload)