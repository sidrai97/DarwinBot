from argsLoader import loadCmdArgs
import mongoCURD
import messageHandler

userid=str(loadCmdArgs(1))
dob=str(loadCmdArgs(2))
weight=str(loadCmdArgs(3))
height=str(loadCmdArgs(4))
location=str(loadCmdArgs(5))
injury=str(loadCmdArgs(6))

mongoCURD.setDetails(userid,dob,weight,height,location,injury)
messageText="Got it 👍.Now please describe your symptoms such as stomach ache, headache or fatigue"
messageHandler.sendTextMessage(userid,messageText)
