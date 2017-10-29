from argsLoader import loadCmdArgs
import messageHandler

eventObject=loadCmdArgs()
senderId=eventObject['sender']['id']
messageText="Can't understand your message"
if 'text' in eventObject['message']:
    messageText=eventObject['message']['text']
messageHandler.sendTextMessage(senderId,messageText)