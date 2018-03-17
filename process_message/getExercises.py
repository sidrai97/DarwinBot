from argsLoader import loadCmdArgs
import mongoCURD

userid=str(loadCmdArgs(1))

level=str(loadCmdArgs(2))
if len(level) == 0:
    level=[]
else:
    level=level.split(",")
muscle=str(loadCmdArgs(3))
if len(muscle) == 0:
    muscle=[]
else:
    muscle=muscle.split(",")
etype=str(loadCmdArgs(4))
if len(etype) == 0:
    etype=[]
else:
    etype=etype.split(",")
equipment=str(loadCmdArgs(5))
if len(equipment) == 0:
    equipment=[]
else:
    equipment=equipment.split(",")
res=mongoCURD.getExercisesQuery(level,muscle,etype,equipment)
print(res)