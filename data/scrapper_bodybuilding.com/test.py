import json
with open('exercises_data.json') as data_file:    
    data = json.load(data_file)
values = data['data']
for k,v in values.items():
    print(k)
    print(len(v))
