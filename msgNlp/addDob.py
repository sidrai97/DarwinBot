from argsLoader import loadCmdArgs
import mongoCURD
import messageHandler

userid=str(loadCmdArgs(1))
dob=str(loadCmdArgs(2))
mongoCURD.updateDOB(userid,dob)
messageText="Now you can continue to tell me about your symptoms eg. stomach ache, headache, etc."
messageHandler.sendTextMessage(userid,messageText)
