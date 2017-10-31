import infermedica_api

def makeApiObj(app_id,app_key):
    return infermedica_api.API(app_id=app_id, app_key=app_key)

def parse(api,msg):
    return api.parse(msg, include_tokens=True)

def suggest():
    return

def diagnosis():
    return

#2 quick buttons
gender=input('\nselect gender:')
age=input('\nenter age:')
api=makeApiObj('3fec2816','73414234b82c58cd63904e19eef2d70e')
response=parse(api,'i feel stretch and pain in calves while walking')
print(response, end="\n\n")
