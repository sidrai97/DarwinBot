import sys
import json
received=json.loads(sys.argv[1])
messageData={
    'recipient':{
        'id': received['id']
    },
    'message':{
        'text': received['msg']['text']
    }
}
print(json.dumps(received))
print(json.dumps(messageData))