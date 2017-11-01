import json
from commonVars import app_url

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

def sendButtonMessage(recipientId):
    messageData={
        'recipient':{
			'id': recipientId
		},
		'message':{
			'attachment':{
				'type':'template',
				'payload':{
					'template_type':'button',
					'text':'I need your date of Birth for symptom checking',
                    'buttons':[
                        {
                            'type':'web_url',
                            'url':app_url+'/enterDob?userid='+recipientId,
                            'title':'Click Here',
                            'webview_height_ratio':'compact'
                        }
                    ]
				}
			}
		}
	}
    sendToNode(messageData)
    return    