import infermedica_api

api = infermedica_api.API(app_id='3fec2816', app_key='73414234b82c58cd63904e19eef2d70e')
request = infermedica_api.Diagnosis(sex='female', age=35)

request.add_symptom('s_21', 'present')
request.add_symptom('s_98', 'present')
request.add_symptom('s_107', 'absent')

# call diagnosis
request = api.diagnosis(request)

print(request)

# ask patient the questions returned by diagnosis and update request with patient answers
request.add_symptom('s_99', 'present')
request.add_symptom('s_8', 'absent')
request.add_symptom('s_25', 'present')
# ... and so on until you decided that enough question have been asked
# or you have sufficient results in request.conditions

# call diagnosis again with updated request
request = api.diagnosis(request)

# repeat the process
print('\n\n', request)