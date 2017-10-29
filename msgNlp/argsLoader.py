import json
import sys

def loadCmdArgs():
    return json.loads(sys.argv[1])