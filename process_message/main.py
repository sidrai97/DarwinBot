import messageHandler, mongoCURD, json, symptomChecker, datetime
from argsLoader import loadCmdArgs
from userProfile import userProfileApi
from commonVars import app_url

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
    elif eventObject['postback']['payload'] == 'symptom_checker':
        buttonsArray=[
            {
                'type':'web_url',
                'url':app_url+'/getDetails?userid='+recipientId,
                'title':'Click Here',
                'webview_height_ratio':'tall'
            }
        ]
        text='Ok but first, I need you to add/update your personal details'
        messageHandler.sendButtonMessage(recipientId,text,buttonsArray)
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
        messageText=eventObject['postback']['payload']
        symptomChecker.userMsgParse(recipientId,messageText,True)
    else:
        messageText="Not sure what you were seeking! No problem try again."
        messageHandler.sendTextMessage(recipientId,messageText)
elif 'message' in eventObject:
    if 'text' in eventObject['message']:
        #symptom_checker
        messageText=eventObject['message']['text']
        symptomChecker.userMsgParse(recipientId,messageText)
else:
    messageHandler.sendTextMessage(recipientId,messageText)