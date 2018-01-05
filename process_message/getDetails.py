from argsLoader import loadCmdArgs
import mongoCURD, datetime

userid=str(loadCmdArgs(1))
details=mongoCURD.getDetails(userid)
dob=details.get('dob',datetime.datetime.today().strftime("%Y-%m-%d"))
weight=details.get('weight',0)
height=details.get('height',0)
location=details.get('location','')
injury=details.get('injury','')
print(userid+':'+dob+':'+str(weight)+':'+str(height)+':'+str(location)+':'+str(injury))
