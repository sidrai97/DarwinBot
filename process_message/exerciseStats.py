from argsLoader import loadCmdArgs
import mongoCURD, json

query=json.loads(str(loadCmdArgs(1)))
userid=query['userid']
exercisename=query['exercisename']
weighttype=query['weighttype']
yaxis=None
if weighttype == "bodyweight":
    yaxis = "reps"
else:
    yaxis = query['yaxis']
details=mongoCURD.getStatsData(userid,exercisename)
final=[]
for a in details:
    if weighttype == a['weighttype']:
        if yaxis == "reps":
            final.append({'logDate':a['logDate'],'freq':a['numberofreps']})
        elif yaxis == "weights" and "weight" in a:
            final.append({'logDate':a['logDate'],'freq':a['weight']})
print(final)