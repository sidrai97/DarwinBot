import infermedicaHandler
from commonVars import infermedica_app_id
from commonVars import infermedica_app_key
from commonVars import diagnosis_threshold
import messageHandler
import json
from copy import deepcopy

def userMsgParse(recipientId,messageText,diagnosisRaw=False):
    api=infermedicaHandler.makeApiObj(infermedica_app_id,infermedica_app_key)
    
    if diagnosisRaw == False:
        #parse user text msg
        response=infermedicaHandler.parse(api,messageText)
        response=response.to_dict()

        if len(response['mentions']) == 0:
            reply="I'm sorry but I didn't understand.\nPlease describe your most important symptoms, for example headache, back pain"
            messageHandler.sendTextMessage(recipientId,reply)
            return
        
        # diagnosis using mentions
        response=infermedicaHandler.diagnosis(recipientId,api,response['mentions'])
        response=response.to_dict()
    else:
        texts=messageText.split('||')
        request=json.loads(texts[2])
        response=infermedicaHandler.diagnosis(recipientId,api,request,True)
        response=response.to_dict()

    # checkthreshold and return
    if len(response['conditions']) >= 3:
        for c in response['conditions']:
            if c['probability'] > diagnosis_threshold:
                cond=api.condition_details(c['id'])
                hint=cond['extras']['hint']
                text='My algorithm says you have symptoms of '+c['common_name']
                messageHandler.sendTextMessage(recipientId,text)
                messageHandler.sendTextMessage(recipientId,hint)
                return

    if response['question']['type'] != 'single':
        reply="I'm sorry but I couldn't find anything relevant at the moment.\nPlease describe your most important symptoms, for example headache, back pain"
        messageHandler.sendTextMessage(recipientId,reply)
        return
    else:
        newId=response['question']['items'][0]['id']
        text=response['question']['text']
        yes=deepcopy(response)
        yes={"sex":yes['sex'],"age":yes['age'],"evidence":yes['evidence']}
        no=deepcopy(yes)
        yes['evidence'].append({"id":str(newId), "choice_id":"present"})
        no['evidence'].append({"id":str(newId), "choice_id":"absent"})
        yes=json.dumps({"symptoms":yes})
        no=json.dumps({"symptoms":no})
        #send yes/no question
        buttonsArray=[
            {
                'type':'postback',
                'title':'Yes',
                'payload':'diagnosis_postback||yes||'+yes
            },
            {
                'type':'postback',
                'title':'No',
                'payload':'diagnosis_postback||no||'+no
            }
        ]
        messageHandler.sendButtonMessage(recipientId,text,buttonsArray)
    return