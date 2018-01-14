import json

def sendToNode(messageData):
    print(json.dumps(messageData))
    return

def sendTextMessage(recipientId, messageText, quickReply=None):
    messageData={
        'recipient':{
            'id': recipientId
        },
        'message':{
            'text': messageText
        }
    }
    # send msg with quick reply buttons
    if(quickReply is not None):
        messageData['message']['quick_replies']=quickReply
    sendToNode(messageData)
    return

def sendButtonMessage(recipientId,text,buttonsArray=None):
    messageData={
        'recipient':{
			'id': recipientId
		},
		'message':{
			'attachment':{
				'type':'template',
				'payload':{
					'template_type':'button',
					'text':text,
                    'buttons':buttonsArray
				}
			}
		}
	}
    sendToNode(messageData)
    return    