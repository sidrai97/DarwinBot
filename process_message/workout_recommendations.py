import mongoCURD,messageHandler
def get_workout_recommendation(recipientId):
    #note for unfit people
    note = "Note: This guidelines are relevant to only healthy individuals or else you should seek medical advice before following these recommendations"
    messageHandler.sendTextMessage(recipientId,note)
    #check age,height,weight from db
    #cal macros needed
    age,gender = mongoCURD.getAgeGender(recipientId)
    if age >= 5 and age <= 17:
        messageText = "1. You should perform atleast 60 minutes of moderate or vigorous intensity aerobic physical activity daily\n\n2. Muscle strengthening activities can be perfromed 3 or more days per week\n\n3. Rest Interval: 30 seconds between sets/laps"
    elif age >= 18 and age <= 64:
        messageText = "1. You should perfrom atleast 75 to 150 minutes of moderate or vigorous intensity aerobic physical activity daily\n\n2. Muscle strengthening activities can be performed 3 or more days per week\n\n3. Rest Interval: 30-45 seconds between sets/laps"
    elif age >= 65:
        messageText = "1. You should perfrom atleast 45 to 60 minutes of moderate intensity aerobic physical activity daily\n\n2. Peform activities to enhance balance and mobility on 3 or more days per week\n\n3. Muscle strengthening activities can be performed 2 or more days per week\n\n4. Rest Interval: 45-60 seconds between sets/laps"
    else:
        messageText = "Atleast 30 min of physical activity is needed"
    messageHandler.sendTextMessage(recipientId,messageText)
    #activity options
    note2 = "You can perform activities such as\n\t1. Walking\n\t2. Running\n\t3. Cycling\n\t4. Swimming\n\t5. Dancing\n\t6. Yoga\n\t7. Weight-training\n\t8. Sports\n\t9. Outdoor Games"
    messageHandler.sendTextMessage(recipientId,note2)
    #note for beginners
    note3 = "Note: Beginners should start with small amounts of physical activity and gradually increase duration, frequency and intensity over time"
    messageHandler.sendTextMessage(recipientId,note3)