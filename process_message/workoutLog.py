from argsLoader import loadCmdArgs
import mongoCURD, messageHandler, json

query=json.loads(str(loadCmdArgs(1)))
userid=query['userid']
del query['userid']
mongoCURD.storeWorkoutLog(userid,query)
messageText="Got it 👍."
messageHandler.sendTextMessage(userid,messageText)
#messageHandler.sendTextMessage(userid,json.dumps(query))