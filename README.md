# DarwinBot - Intelligent Health Assistant

Facebook Messenger Chatbot with symptom checker, workout recommendation, exercise encyclopedia, workout log and statistics.

#### Install NodeJS, MongoDB and Python

#### To download all Node dependencies run
```
npm install
```
#### To download all Python dependencies run
```
pip install requirements.txt
```

#### Create a facebook developer account and a facebook page

#### Under the developer console

#### Create new App and select messenger platform

#### Select the page you had created earlier and generate access_token

#### Subscribe to following page events
```
message event, postback event, delivery event
```

#### Setup webhook URL using ngrok and create verify_token

#### Create developer account on Infermedica and get app_id and app_key

#### Start the Node server
```
node ./DarwinBot/index.js
```

#### Start the MongoDB server
```
mongod --dbpath=./DarwinBot/db
```

#### Chatbot ready to use from Facebook messenger
