from argsLoader import loadCmdArgs
import mongoCURD, datetime

userid=str(loadCmdArgs(1))
details=mongoCURD.getExerciseNames(userid)
print(details)