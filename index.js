'use strict'
//heroku URL: https://salty-journey-37615.herokuapp.com/webhook/
const express = require('express')
const bodyParser = require('body-parser')
const request = require('request')
const PythonShell = require('python-shell')

const app = express()
const token = (process.env.FB_VERIFY_TOKEN)
const access = (process.env.FB_ACCESS_TOKEN)
const windowCloseUrl = "https://www.messenger.com/closeWindow/?image_url=https://scontent-bom1-1.xx.fbcdn.net/v/t1.0-9/22894529_1542725419106506_7073729451153698249_n.jpg?oh=749bddcf82ff0e41ccd1c74f6d75fcf5&oe=5AEE6884&display_text=Thankyou"

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

app.get('/getDetails', function(req, resp){
	var userid=req.query.userid
	var pypath = './process_message/getDetails.py'
	var options = {mode:'text',args:[userid]}
	PythonShell.run(pypath,options,function(err,results){
		if(err) throw err
		if(results.length > 0){
			var messageData=results[0].trim().split(':')
			resp.render('detailsView', {userid:messageData[0],dob:messageData[1],weight:messageData[2],height:messageData[3],location:String(messageData[4]),injury:messageData[5]})
			console.log("received from python : "+messageData)
		}
		else{
			resp.send('ID not found!')
		}
	})
})

app.get('/setDetails', function(req, resp){
	var userid=req.query.userid
	var dob=req.query.dob
	var weight=req.query.weight
	var height=req.query.height
	var location=req.query.location
	var injury=req.query.injury
	if(injury == undefined)
		injury=[]
	
	var pypath = './process_message/addDetails.py'
	var options = {mode:'text',args:[userid,dob,weight,height,location,injury]}
	PythonShell.run(pypath,options,function(err,results){
		if(err) throw err
		for(var idx=0; idx<results.length; idx++){
			var messageData=JSON.parse(results[idx])
			console.log("received from python : "+messageData)
			callSendAPI(messageData)
			setTimeout(function(){},1000)
		}
	})
	//close the webview
	resp.redirect(windowCloseUrl)
	//resp.send("Thankyou for your cooperation!!")
})

// show webview for suggestions
app.get('/getSuggestions', function(req,resp){
	var userid=req.query.userid
	var suggestions=JSON.parse(req.query.suggestions)
	resp.render('symptomSuggestion', {userid:userid, suggestions:suggestions})
})

// pass on the selected options from suggestions for further diagnosis
app.get('/setSuggestions', function(req,resp){
	var userid=req.query.userid
	delete req.query.userid
	var suggestionSelected=""
	for(var key in req.query){
		suggestionSelected+=req.query[key]+" "
	}
	// python execution
	var pypath = './process_message/setSuggestions.py'
	var options = {mode:'text',args:[userid,suggestionSelected]}
	PythonShell.run(pypath,options,function(err,results){
		if(err) throw err
		for(var idx=0; idx<results.length; idx++){
			var messageData=JSON.parse(results[idx])
			console.log("received from python : "+messageData)
			callSendAPI(messageData)
			setTimeout(function(){},1000)
		}
	})
	//close the webview
	resp.redirect(windowCloseUrl)
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