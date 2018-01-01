import getHtml
soup=getHtml.getHtmlFromUrl('https://www.bodybuilding.com/exercises/')
soup=soup.find('section',class_='exercise-list-container')
soup=soup.find_all('a')
s=''
for tag in soup:
    s+=tag['href']+'\n'
fhand=open('musclesLinks.txt','w')
fhand.write(s)
fhand.close()