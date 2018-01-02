'use strict'
//heroku URL: https://salty-journey-37615.herokuapp.com/webhook/
const express = require('express')
const bodyParser = require('body-parser')
const request = require('request')
const PythonShell = require('python-shell')

const app = express()
const token = (process.env.FB_VERIFY_TOKEN)
const access = (process.env.FB_ACCESS_TOKEN)

app.set('port', (process.env.PORT || 5000)) 
app.set('view engine', 'pug')

// Allows us to process the data
app.use(bodyParser.urlencoded({extended: false}))	
app.use(bodyParser.json())

// ROUTES
app.get('/', function(req, res) {
	res.send("Hi, I am Darwin - Intelligent Health Assistant!")
})

app.get('/webhook', function(req, res) {
	if (req.query['hub.mode'] === 'subscribe' && req.query['hub.verify_token'] === token){
		console.log("Validating webhook")
		res.status(200).send(req.query['hub.challenge'])
	} 
	else{
	  console.error("Failed validation. Make sure the validation tokens match.")
	  res.sendStatus(403)      
	}  
})

app.post('/webhook', function (req, res) {
	var data = req.body
	// Make sure this is a page subscription
	if (data.object === 'page') {
		// Iterate over each entry - there may be multiple if batched
		data.entry.forEach(function(entry) {
			var pageID = entry.id
			var timeOfEvent = entry.time
			// Iterate over each messaging event
			entry.messaging.forEach(function(event) {
                if (event.message) {
					receivedMessage(event)
					console.log("Webhook received message event: ", event)
                }
                else if (event.postback){
                    receivedMessage(event)
                    console.log("Webhook received postback event: ", event)
                } 
                else {
                    console.log("Webhook received unknown event: ", event)
                }
			})
		})
		res.sendStatus(200)
	}
})

app.get('/enterDob', function(req, resp) {
	var userid=req.query.userid
	resp.render('dobView', {userid:userid})
})

app.get('/storeDob', function(req, resp){
	var userid=req.query.userid
	var dob=req.query.dob
	console.log(userid)
	console.log(dob)
	var pypath = './process_message/addDob.py'
	var options = {mode:'text',args:[userid,dob]}
	PythonShell.run(pypath,options,function(err,results){
		if(err) throw err
		for(var idx=0; idx<results.length; idx++){
			var messageData=JSON.parse(results[idx])
			console.log("received from python : "+messageData)
			callSendAPI(messageData)
			setTimeout(function(){},1000)
		}
	})
	resp.send("Thankyou for your cooperation!!")
})

// Send Message to Facebook
function callSendAPI(messageData) {
	request({
		uri: 'https://graph.facebook.com/v2.6/me/messages',
		qs: { access_token: access },
		method: 'POST',
		json: messageData
	}, function (error, response, body) {
		if (!error && response.statusCode == 200) {
			var recipientId = body.recipient_id
			var messageId = body.message_id
			console.log("Successfully sent the message with id %s to recipient %s", messageId, recipientId)
		} 
		else {
			console.error("Unable to send message.")
			console.error(response)
			console.error(error)
		}
	})
}

//sending received message to python script
function receivedMessage(event){
	var pypath = './process_message/main.py'
	var options = {mode:'text',args:[JSON.stringify(event)]}
	PythonShell.run(pypath,options,function(err,results){
		if(err) throw err
		for(var idx=0; idx<results.length; idx++){
			var messageData=JSON.parse(results[idx])
			console.log("received from python : "+messageData)
			callSendAPI(messageData)
			setTimeout(function(){},7000);
		}
	})
}

// run app
app.listen(app.get('port'), function() {
	console.log("running: "+app.get('port'))
})