import sys
import json

def loadCmdArgs():
    return json.loads(sys.argv[1])

def sendTextMessage(recipientId, messageText, quickReply=None):
    messageData={
        'recipient':{
            'id': recipientId
        },
        'message':{
            'text': messageText
        }
    }
    if(quickReply is not None):
        messageData['message']['quick_replies']=quickReply
    print(json.dumps(messageData))
    exit()

event=loadCmdArgs()
senderId=event['sender']['id']
messageText=event['message']['text']
sendTextMessage(senderId,messageText)