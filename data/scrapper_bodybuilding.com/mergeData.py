import json
with open('exercises_data.json') as data_file:    
    data = json.load(data_file)
temp = data['data']
for idx in range(1,16):
    with open('exercises_data'+str(idx)+'.json') as data_file2:    
        data2 = json.load(data_file2)
    data2=data2['data']
    key=list(data2.keys())[0]
    val=list(data2.values())[0]
    temp[key]=val
fhand=open('exercises_data.json','w')
fhand.write(json.dumps(data))
fhand.close()
print('done')