import urllib
from bs4 import BeautifulSoup

def getHtmlFromUrl(url):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html,'html5lib')    
    return soup