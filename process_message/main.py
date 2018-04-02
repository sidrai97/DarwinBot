import sys
sys.path.append("C:/Users/sid/Desktop/Darwin/DarwinBot/process_message/intentClassifier")
import messageHandler, mongoCURD, json, symptomChecker, commonVars, predict_merge, textblob, workout_recommendations
from argsLoader import loadCmdArgs
from userProfile import userProfileApi

#load eventObj from command Line
eventObject=json.loads(loadCmdArgs())

# userId from eventObj
recipientId=eventObject['sender']['id']

# fallback msg
messageText="I'm sorry but I didn't understand. Please Try Again!"

# 
if 'postback' in eventObject:
    if eventObject['postback']['payload'] == 'get_started':
        messageText="Hi! I'm Darwin your personal Health Assistant.\nI can help you achieve your goal of 'Good Health'.\nTo know more checkout the 'Menu'."
        messageHandler.sendTextMessage(recipientId,messageText)
        # get userProfile and make an entry of user in db
        mongoCURD.insertUserDataFromFb(userProfileApi(recipientId))
        buttonsArray=[
            {
                'type':'web_url',
                'url':commonVars.app_url+'/getDetails?userid='+recipientId,
                'title':'Click Here',
                'webview_height_ratio':'compact',
                'webview_share_button':'hide'
            }
        ]
        text='I need you to add/update your personal details'
        messageHandler.sendButtonMessage(recipientId,text,buttonsArray)
    elif eventObject['postback']['payload'] == "update_info":    
        buttonsArray=[
            {
                'type':'web_url',
                'url':commonVars.app_url+'/getDetails?userid='+recipientId,
                'title':'Click Here',
                'webview_height_ratio':'compact',
                'webview_share_button':'hide'
            }
        ]
        text='To add/update your personal details click the button attached'
        messageHandler.sendButtonMessage(recipientId,text,buttonsArray)
    elif eventObject['postback']['payload'] == 'symptom_checker':
        messageText="Make sure i have your updated info. And then describe your symptoms such as stomach ache, headache or fatigue"
        messageHandler.sendTextMessage(recipientId,messageText)
    elif eventObject['postback']['payload'] == 'plan_my_workout':
        buttonsArray=[
            {
                'type':'web_url',
                'url':commonVars.app_url+'/workoutLog',
                'title':'Click Here',
                'webview_height_ratio':'tall',
                'webview_share_button':'hide'
            }
        ]
        text='Lets update your Workout Log'
        messageHandler.sendButtonMessage(recipientId,text,buttonsArray)
    elif eventObject['postback']['payload'] == 'get_workout_recommendations':
        workout_recommendations.get_workout_recommendation(recipientId)
    elif eventObject['postback']['payload'] == 'my_workout_statistics':
        messageText="Feature coming soon!"
        messageHandler.sendTextMessage(recipientId,messageText)
    elif eventObject['postback']['payload'] == 'exercise_encyclopedia':
        buttonsArray=[
            {
                'type':'web_url',
                'url':commonVars.app_url+'/getExerciseEncyclopedia?userid='+recipientId,
                'title':'Door to 💪 knowledge',
                'webview_height_ratio':'tall',
                'webview_share_button':'hide'
            }
        ]
        text="To open the Encyclopedia you have to click the button below!!"
        messageHandler.sendButtonMessage(recipientId,text,buttonsArray)
    elif 'diagnosis_postback||' in eventObject['postback']['payload']:
        postback_payload = eventObject['postback']['payload'].split("||")
        qid = postback_payload[2]
        option = postback_payload[1]
        temp=[]
        if option == "yes":
            temp.append({'id': qid, 'choice_id': 'present'})
        elif option == "no":
            temp.append({'id': qid, 'choice_id': 'absent'})
        else:
            temp.append({'id': qid, 'choice_id': 'unknown'})
        payload=mongoCURD.getSymptomPayload(recipientId)
        payload["symptoms_payload"]["evidence"]+=temp
        symptomChecker.diagnosisHandler(recipientId,payload)
    else:
        messageText="Not sure what you were seeking! No problem try again."
        messageHandler.sendTextMessage(recipientId,messageText)
elif 'message' in eventObject:
    if 'text' in eventObject['message']:
        #symptom_checker
        messageText=eventObject['message']['text']
        messageText=messageText.lower()
        
        #spelling message correction
        messageText=textblob.TextBlob(messageText)
        messageText=str(messageText.correct())
        
        #Identify user message intent
        label = predict_merge.predict_unseen_data(messageText)
        if label == "symptom_checker":
            symptomChecker.parseSuggest(recipientId,messageText)
        elif label == "exercise_encyclopedia":
            buttonsArray=[
                {
                    'type':'web_url',
                    'url':commonVars.app_url+'/getExerciseEncyclopedia?userid='+recipientId,
                    'title':'Door to 💪 knowledge',
                    'webview_height_ratio':'tall',
                    'webview_share_button':'hide'
                }
            ]
            text="To open the Encyclopedia you have to click the button below!!"
            messageHandler.sendButtonMessage(recipientId,text,buttonsArray)
        elif label == "plan_workout":
            messageHandler.sendTextMessage(recipientId,label)
        elif label == "progress_stats":
            messageHandler.sendTextMessage(recipientId,label)
        elif label == "update_details":
            buttonsArray=[
                {
                    'type':'web_url',
                    'url':commonVars.app_url+'/getDetails?userid='+recipientId,
                    'title':'Click Here',
                    'webview_height_ratio':'compact',
                    'webview_share_button':'hide'
                }
            ]
            text='To add/update your personal details click the button attached'
            messageHandler.sendButtonMessage(recipientId,text,buttonsArray)
        elif label == "workout_recommendation":
            workout_recommendations.get_workout_recommendation(recipientId)
        elif label == "help":
            messageText = "Hi! I'm Darwin your health assistant\nAnd i can help you with the following things:\n\t1. Symptom checking\n\t2. Exercises Information\n\t3. Exercises Recommendation\n\t4. Workout log\n\t5. Workout Statistics\nUse the given buttons or simply type your query and send it to me"
            messageHandler.sendTextMessage(recipientId,messageText)
        elif label == "greetings":
            greets=['Hi','Hey','Heya','Yoo','Hello']
            from random import randint
            messageText = greets[randint(0,len(greets)-1)]+', Lets begin!!'
            messageHandler.sendTextMessage(recipientId,messageText)
        elif label == "end_conversation":
            messageText = 'Bye!!'
            messageHandler.sendTextMessage(recipientId,messageText)
else:
    messageHandler.sendTextMessage(recipientId,messageText)