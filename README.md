# DarwinBot - Intelligent Health Assistant

Facebook Messenger Chatbot with symptom checker, workout recommendation, exercise encyclopedia, workout log and statistics.

### Execution Steps

1. Install NodeJS, MongoDB and Python

2. To download all Node dependencies run
```
npm install
```

3. To download all Python dependencies run
```
pip install requirements.txt
```

4. Create a facebook developer account and a facebook page

5. Under the developer console

6. Create new App and select messenger platform

7. Select the page you had created earlier and generate access_token

8. Subscribe to following page events
```
message event, postback event, delivery event
```

9. Setup webhook URL using ngrok and create verify_token

10. Create developer account on Infermedica and get app_id and app_key

11. Start the Node server
```
node ./DarwinBot/index.js
```

12. Start the MongoDB server
```
mongod --dbpath=./DarwinBot/db
```

13. Chatbot ready to use from Facebook messenger
