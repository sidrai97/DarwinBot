from urllib import request, parse
from bs4 import BeautifulSoup
import json
muscle_ids=['chest','forearms','lats','middle-back','lower-back','neck','quadriceps',
'hamstrings','calves','triceps','traps','shoulders','abdominals','glutes','biceps']
muscle_exercises=[]
for count in range(1,16):
    page=0
    all_links=[]
    while(True):   
        print('id:{}'.format(count))
        print('page:{}'.format(page)) 
        mydict={"params":"muscleID="+str(count)+";exerciseTypeID=2,6,4,7,1,3,5;equipmentID=9,14,2,10,5,6,4,15,1,8,11,3,7;mechanicTypeID=1,2,11",
        "orderByField":"exerciseName","orderByDirection":"ASC","page":page}
        url='https://www.bodybuilding.com/exercises/ajax/getfinderdata/'
        data = parse.urlencode(mydict).encode()
        req =  request.Request(url, data=data) # this will make the method "POST"
        try:
            resp = request.urlopen(req)
        except:
            print('jhol hua!')    
            exit()
        soup = BeautifulSoup(resp,'html5lib')   
        temp=soup.find_all('a')
        links=[]
        for i in temp:
            s=i['href']
            s=s.strip('\\"')
            s=s.replace('\\','')
            if '/detail/view' in s and s not in links:
                links.append(s)
        if len(links) < 1:
            break
        for link in links:
            all_links.append(link)
        page+=15
    print(len(all_links))
    muscle_exercises.append(all_links)

fhand=open('exercises_links.json','w')
fhand.write(json.dumps({'data':{'keys':muscle_ids,'values':muscle_exercises}}))
fhand.close()