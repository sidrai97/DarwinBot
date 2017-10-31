from argsLoader import loadCmdArgs
import messageHandler

#load eventObj from command Line
eventObject=loadCmdArgs()

# userId from eventObj
senderId=eventObject['sender']['id']

# fallback msg
messageText="Can't understand your message"

# 
if 'text' in eventObject['message']:
    messageText=eventObject['message']['text']
    messageHandler.sendTextMessage(senderId,messageText)
elif eventObject['postback']['payload'] == 'get_started'
    messageText="Hi! I'm Darwin your personal Health Assistant. I can help you achieve your goal of 'Good Health'. To know more checkout the 'Features Menu' or simply say 'help'."
    messageHandler.sendTextMessage(senderId,messageText)
else:
    messageHandler.sendTextMessage(senderId,messageText)