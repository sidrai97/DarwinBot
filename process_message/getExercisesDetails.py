from argsLoader import loadCmdArgs
import mongoCURD, messageHandler, json, commonVars

userid=str(loadCmdArgs(1))
eid=str(loadCmdArgs(2))
res=mongoCURD.getExercisesDetails(eid)
res=res[0]
elements=[
    {
        'title':res['name'],
        'subtitle':"Start Position",
        'image_url':res['left_img_url'],     
        'default_action':{
            'type':"web_url",
            'url':res['left_img_url'],
            'webview_height_ratio':"tall",
            'webview_share_button':'hide'
        } 
    },
    {
        'title':res['name'],
        'subtitle':"End Position",
        'image_url':res['right_img_url'],
        'default_action':{
            'type':"web_url",
            'url':res['right_img_url'],
            'webview_height_ratio':"tall",
            'webview_share_button':'hide'
        }
    }
]
messageText="Exercise: 	"+res["name"]+"\n\nMuscle: "+res["muscle"]+"\n\nLevel: "+res["level"]+"\n\nEquipment: "+res["equipment"]
buttonsArray=[
    {
        'type':'web_url',
        'url':commonVars.app_url+'/viewSteps?name='+res['name']+'&steps='+json.dumps(res['guide']),
        'title':'Steps',
        'webview_height_ratio':'tall',
        'webview_share_button':'hide'
    },
    {
        'type':"web_url",
        'url':res['video_url'],
        'title':"Video",
		'webview_height_ratio': "full",
        'webview_share_button':'hide'
    }
]
messageHandler.sendButtonMessage(userid,messageText,buttonsArray)
messageHandler.sendGenericMessage(userid,elements)