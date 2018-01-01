import getHtml
import json

with open('exercises_links.json') as data_file:    
    data = json.load(data_file)
values = data['data']['values']
keys = data['data']['keys']
count=0
index=int(input('enter index : '))
key=keys[index]
with open('exercises_data'+str(index+1)+'.json') as data_file:    
    data=json.load(data_file)
data['data'][key]=[]
fhand=open('exercises_data'+str(index+1)+'.json','w')
fhand.write(json.dumps(data))
fhand.close()
for url in values[index]:
    try:
        soup=getHtml.getHtmlFromUrl(url)
        guide=soup.find('div',class_='guideContent')
        steps=guide.find_all('li')
        details=soup.find('div',id='exerciseDetails')
        exercise={}
        steps_text=[] # steps
        for s in steps:
            s=s.text.strip()
            s=s.replace('  ',' ')
            steps_text.append(s)
        exercise['guide']=steps_text
        exercise['name']=details.h1.text.strip() #exercise name
        edetails=details.find_all('span')
        for i in edetails:
            ch=i.text
            ch=ch.replace(' ','')
            ch=ch.replace(':',' ')
            ch=ch.replace('\n','')
            ch=ch.lower().split()
            if ch[0] == 'mainmuscleworked':
                ch[0]='muscle'
            exercise[ch[0]]=ch[1].lower()
        left=soup.find('div',class_='photoLeft')
        right=soup.find('div',class_='photoRight')
        left=left.find('a')['href']
        right=right.find('a')['href']
        exercise['left_img_url']=left
        exercise['right_img_url']=right
        video=soup.find('div',id='maleVideo')
        video='https:'+video.find('source')['src']
        exercise['video_url']=video
        #print(exercise)
        with open('exercises_data'+str(index+1)+'.json') as data_file:    
            data=json.load(data_file)
        data['data'][key].append(exercise)
        fhand=open('exercises_data'+str(index+1)+'.json','w')
        fhand.write(json.dumps(data))
        fhand.close()
        count+=1
    except:
        print(url)
print(count)