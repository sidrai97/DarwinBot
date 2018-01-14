import requests, os, json, mongoCURD, messageHandler, commonVars

def getApiUrl():
	return 'https://api.infermedica.com/v2/'

def getHeaders():
	return {'app-id': os.getenv('INFERMEDICA_APP_ID'), 'app-key': os.getenv('INFERMEDICA_APP_KEY'), 'content-type': 'application/json', 'accept': 'application/json'}

def parseEndpoint(messageText):
	r = requests.post(getApiUrl()+'parse', data=json.dumps({'text':messageText}), headers=getHeaders())
	mentions = r.json()['mentions']
	evidence=[]
	for m in mentions:
		evidence.append({'id':m['id'],'choice_id':m['choice_id'],'initial':True})
	return (evidence,mentions)

def calcBMI(weight,height):
	return int(weight/(height*height))

def getRiskFactors(userid):
	res = mongoCURD.getDetails(userid)
	gender = res['gender']
	age = mongoCURD.ageCalc(res['dob'])
	bmi = calcBMI(float(res['weight']),float(res['height']))
	injury = res['injury'].split(',')
	evidence = [{'id':res['location'],'choice_id':'present','initial':True}]
	if bmi < 19:
		evidence.append({'id':'p_6','choice_id':'present','initial':True})
	elif bmi > 30:
		evidence.append({'id':'p_7','choice_id':'present','initial':True})
	if injury[0] != '':
		for i in injury:
			evidence.append({'id':i,'choice_id':'present','initial':True})
	return (gender,age,evidence)

def suggestEndpoint(gender,age,evidence):
	payload = {'sex':gender, 'age':age, 'evidence':evidence}
	r = requests.post(getApiUrl()+'suggest', data=json.dumps(payload), headers=getHeaders())
	suggestedSymptoms = r.json()
	for s in suggestedSymptoms:
		s['name']=s['common_name']
		del(s['common_name'])
	return suggestedSymptoms

def parseSuggest(userid,messageText):
	# find mentions
	temp,mentions = parseEndpoint(messageText)
	# if no mentions found than fallback
	if len(temp) == 0:
		messageText = "Sorry, I am not able to identify any symptoms/conditions from your message. Please try again!"
		messageHandler.sendTextMessage(userid,messageText)
		return
	# get user details from db
	gender,age,evidence = getRiskFactors(userid)
	evidence += temp
	# get suggestions based on mentions
	suggestedSymptoms = suggestEndpoint(gender,age,evidence)
	if len(suggestedSymptoms) < 1:
		# yaha se jaega diagnosis
		messageText = "kuch nai mila"
		messageHandler.sendTextMessage(userid,messageText)
		return
	# send mentions found and suggest more symtoms
	messageText = "You have reported\n"
	for i in mentions:
		messageText += " * "+i["common_name"]+"\n"
	messageText += "Other users with your symptoms also reported following conditions"
	payload = {'sex':gender, 'age':age, 'evidence':evidence}
	mongoCURD.setSymptomPayload(userid,payload)
	buttonsArray=[
		{
			'type':'web_url',
			'url':commonVars.app_url+'/getSuggestions?userid='+userid+'&suggestions='+json.dumps(suggestedSymptoms),
			'title':'Options Here!',
			'webview_height_ratio':'compact',
			'webview_share_button':'hide'
		}
    ]
	messageHandler.sendButtonMessage(userid,messageText,buttonsArray)
	return

def diagnosisEndpoint():
	return