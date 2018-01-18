import messageHandler, mongoCURD, json, symptomChecker, commonVars
from argsLoader import loadCmdArgs
from userProfile import userProfileApi

#load eventObj from command Line
eventObject=json.loads(loadCmdArgs())

# userId from eventObj
recipientId=eventObject['sender']['id']

# fallback msg
messageText="I'm sorry but I didn't understand. Please Try Again!"

# 
if 'postback' in eventObject:
    if eventObject['postback']['payload'] == 'get_started':
        messageText="Hi! I'm Darwin your personal Health Assistant.\nI can help you achieve your goal of 'Good Health'.\nTo know more checkout the 'Menu'."
        messageHandler.sendTextMessage(recipientId,messageText)
        # get userProfile and make an entry of user in db
        mongoCURD.insertUserDataFromFb(userProfileApi(recipientId))
        buttonsArray=[
            {
                'type':'web_url',
                'url':commonVars.app_url+'/getDetails?userid='+recipientId,
                'title':'Click Here',
                'webview_height_ratio':'compact',
                'webview_share_button':'hide'
            }
        ]
        text='I need you to add/update your personal details'
        messageHandler.sendButtonMessage(recipientId,text,buttonsArray)
    elif eventObject['postback']['payload'] == "update_info":    
        buttonsArray=[
            {
                'type':'web_url',
                'url':commonVars.app_url+'/getDetails?userid='+recipientId,
                'title':'Click Here',
                'webview_height_ratio':'compact',
                'webview_share_button':'hide'
            }
        ]
        text='To add/update your personal details click the button attached'
        messageHandler.sendButtonMessage(recipientId,text,buttonsArray)
    elif eventObject['postback']['payload'] == 'symptom_checker':
        messageText="Make sure i have your updated info. And then describe your symptoms such as stomach ache, headache or fatigue"
        messageHandler.sendTextMessage(recipientId,messageText)
    elif eventObject['postback']['payload'] == 'plan_my_workout':
        messageText="Feature coming soon!"
        messageHandler.sendTextMessage(recipientId,messageText)
    elif eventObject['postback']['payload'] == 'get_workout_recommendations':
        messageText="Feature coming soon!"
        messageHandler.sendTextMessage(recipientId,messageText)
    elif eventObject['postback']['payload'] == 'my_workout_statistics':
        messageText="Feature coming soon!"
        messageHandler.sendTextMessage(recipientId,messageText)
    elif eventObject['postback']['payload'] == 'exercises_guide':
        messageText="Feature coming soon!"
        messageHandler.sendTextMessage(recipientId,messageText)
    elif 'diagnosis_postback||' in eventObject['postback']['payload']:
        postback_payload = eventObject['postback']['payload'].split("||")
        qid = postback_payload[2]
        option = postback_payload[1]
        temp=[]
        if option == "yes":
            temp.append({'id': qid, 'choice_id': 'present'})
        elif option == "no":
            temp.append({'id': qid, 'choice_id': 'absent'})
        else:
            temp.append({'id': qid, 'choice_id': 'unknown'})
        payload=mongoCURD.getSymptomPayload(recipientId)
        payload["symptoms_payload"]["evidence"]+=temp
        symptomChecker.diagnosisHandler(userid,payload)
    else:
        messageText="Not sure what you were seeking! No problem try again."
        messageHandler.sendTextMessage(recipientId,messageText)
elif 'message' in eventObject:
    if 'text' in eventObject['message']:
        #symptom_checker
        messageText=eventObject['message']['text']
        '''
        Identify user message intent part remaining
        '''
        symptomChecker.parseSuggest(recipientId,messageText)
else:
    messageHandler.sendTextMessage(recipientId,messageText)