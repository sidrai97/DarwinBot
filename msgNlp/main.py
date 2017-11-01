from argsLoader import loadCmdArgs
import messageHandler
from userProfile import userProfileApi
import mongoCURD
import json

#load eventObj from command Line
eventObject=json.loads(loadCmdArgs())

# userId from eventObj
recipientId=eventObject['sender']['id']

# fallback msg
messageText="I'm sorry but I didn't understand."

# 
if 'postback' in eventObject:
    if eventObject['postback']['payload'] == 'get_started':
        #messageText=userProfileApi(recipientId)
        #messageHandler.sendTextMessage(recipientId,messageText)
        messageText="Hi! I'm Darwin your personal Health Assistant.\nI can help you achieve your goal of 'Good Health'.\nTo know more checkout the 'Features Menu' or simply say 'help'."
        messageHandler.sendTextMessage(recipientId,messageText)
        # get userProfile and make an entry of user in db
        mongoCURD.insertUserData(userProfileApi(recipientId))
    elif eventObject['postback']['payload'] == 'symptom_checker':
        if mongoCURD.checkDOBExists(recipientId):
            messageText="Ok so tell me about your symptoms eg. stomach ache, headache, etc."
            messageHandler.sendTextMessage(recipientId,messageText)
        else:    
            messageHandler.sendButtonMessage(recipientId)
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
elif 'message' in eventObject:
    if 'text' in eventObject['message']:
        #symptom_checker
else:
    messageHandler.sendTextMessage(recipientId,messageText)