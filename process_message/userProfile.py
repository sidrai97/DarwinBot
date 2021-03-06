import requests
import os
import json

def userProfileApi(user_page_id):
    token=os.getenv('FB_ACCESS_TOKEN')
    payload={'access_token': token}
    r=requests.get('https://graph.facebook.com/v2.6/'+user_page_id, params=payload)
    userData=r.json()
    userData['_id']=userData.pop('id')
    return userData