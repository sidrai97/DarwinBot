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
        messageText="Hi! I'm Darwin your personal Health Assistant."
        messageHandler.sendTextMessage(recipientId,messageText)
        messageText="I can help you achieve your goal of 'Good Health'."
        messageHandler.sendTextMessage(recipientId,messageText)
        messageText="To know more checkout the 'Features Menu' or simply say 'help'."
        messageHandler.sendTextMessage(recipientId,messageText)
        # get userProfile and make an entry of user in db
        mongoCURD.insertUserData(userProfileApi(recipientId))
    elif eventObject['postback']['payload'] == 'symptom_checker':
        messageHandler.sendButtonMessage(recipientId)
    elif eventObject['postback']['payload'] == 'plan_my_workout':
        pass
    elif eventObject['postback']['payload'] == 'get_workout_recommendations':
        pass
    elif eventObject['postback']['payload'] == 'my_workout_statistics':
        pass
    elif eventObject['postback']['payload'] == 'exercises_guide':
        pass
elif 'message' in eventObject:
    if 'text' in eventObject['message']:
        #echo text msg
        messageText=eventObject['message']['text']
        messageHandler.sendTextMessage(recipientId,messageText)
else:
    messageHandler.sendTextMessage(recipientId,messageText)