import json
import infermedica_api
from commonVars import infermedica_app_id
from commonVars import infermedica_app_key

def makeApiObj(app_id,app_key):
    return infermedica_api.API(app_id=app_id, app_key=app_key)

def parse(api,msg):
    #id,choice_id,type
    return api.parse(msg, include_tokens=True)

def suggest():
    return

def diagnosis():
    return

api=makeApiObj(infermedica_app_id,infermedica_app_key)

'''
response=parse(api,'i feel stretch and pain in calves while walking')
response=response.to_dict()
#print(response, end="\n\n")


request = infermedica_api.Diagnosis(sex='male', age=20)
for obj in response['mentions']:
    if obj['type'] == 'symptom':
        request.add_symptom(obj['id'], obj['choice_id'])

request.add_symptom('s_83','present')
request.add_symptom('s_735','present')
request.add_symptom('s_44','absent')
request.add_symptom('s_325','absent')
request.add_symptom('p_8','present')

w1=request.to_json()
w2=json.loads(w1)
w2=infermedica_api.Diagnosis(w2)
print(dir(request))
exit()

response=api.diagnosis(request)
print(response, end="\n\n")
response=response.to_dict()
'''
request={
  "sex": "male",
  "age": 20,
  "evidence": [
    {
      "id": "s_232",
      "choice_id": "present"
    },
    {
        "id":"p_53",
        "choice_id":"absent"
    },
    {
        "id":"p_8",
        "choice_id":"absent"
    }
  ]
}
#request=infermedica_api.Diagnosis(request)
#response=api.diagnosis(request)
#response=response.to_dict()
#print(response)
#print(api.condition_details('c_221'))
# severe headaches, light sensitivity and a stiff neck

request = infermedica_api.Diagnosis(sex='female', age=35)

request.add_symptom('s_10', 'present')
request.add_symptom('s_608', 'present')
request.add_symptom('s_1394', 'absent')
request.add_symptom('s_216', 'present')
request.add_symptom('s_9', 'present')
request.add_symptom('s_188', 'present')

# call the explain method
request = api.explain(request, target_id='c_62')

# and see the results
print('\n\n', request)