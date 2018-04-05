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

//Exercise Encyclopedia
app.get('/getExerciseEncyclopedia', function(req, resp){
	var userid=req.query.userid
	resp.render('exerciseEncyclopedia', {userid:userid})
})
app.get('/setExerciseEncyclopedia', function(req, resp){
	var userid=req.query.userid
	var level=req.query.level
	if(level == undefined)
		level=""
	else if(typeof level == "object")
	{
		var temp="";
		for(var i = 0; i < level.length; i++) 
		{
			if(i == 0){temp=level[i];}
			else{temp=temp+","+level[i];}
		}
		level=temp;
	}
	var muscle=req.query.muscle
	if(muscle == undefined)
		muscle=""
	else if(typeof muscle == "object")
	{
		var temp="";
		for(var i = 0; i < muscle.length; i++) 
		{
			if(i == 0){temp=muscle[i]}
			else{temp=temp+","+muscle[i];}
		}
		muscle=temp;
	}
	var type=req.query.type
	if(type == undefined)
		type=""
	else if(typeof type == "object")
	{
		var temp="";
		for(var i = 0; i < type.length; i++) 
		{
			if(i == 0){temp=type[i];}
			else{temp=temp+","+type[i];}
		}
		type=temp;
	}
	var equipment=req.query.equipment
	if(equipment == undefined)
		equipment=""
	else if(typeof equipment == "object")
	{
		var temp="";
		for(var i = 0; i < equipment.length; i++) 
		{
			if(i == 0){temp=equipment[i];}
			else{temp=temp+","+equipment[i];}
		}
		equipment=temp;
	}
	var pypath = './process_message/getExercises.py'
	var options = {mode:'text',args:[userid,level,muscle,type,equipment]}
	PythonShell.run(pypath,options,function(err,results){
		if(err) throw err
		for(var idx=0; idx<results.length; idx++){
			var messageData=results[idx]
			messageData=messageData.replace(/'/g,'"')
			messageData=JSON.parse(messageData)
			if(messageData.length > 0)
				resp.render('exerciseResults', {userid:userid,edata:messageData})
			else
				resp.send('No data found! Try Again...')
		}
	})
})
app.get('/getExerciseDetails', function(req, resp){
	var userid=req.query.userid
	var id=req.query.id
	var pypath = './process_message/getExercisesDetails.py'
	var options = {mode:'text',args:[userid,id]}
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
app.get('/viewSteps', function(req, resp){
	var name=req.query.name
	var steps=req.query.steps
	//console.log(steps)
	steps=JSON.parse(steps)
	resp.render('viewSteps', {name:name,steps:steps})
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

app.get('/groupSingle', function(req, resp){
	var userid=req.query.userid
	var options=JSON.parse(req.query.options)
	resp.render('groupSingle', {userid:userid, options:options})
})
app.get('/groupMultiple', function(req, resp){
	var userid=req.query.userid
	var options=JSON.parse(req.query.options)
	resp.render('groupMultiple', {userid:userid, options:options})
})
app.get('/setGroupSingle', function(req,resp){
	var userid=req.query.userid
	var optionSelected=req.query.single
	// python execution
	var pypath = './process_message/setGroupSingle.py'
	var options = {mode:'text',args:[userid,optionSelected]}
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
app.get('/setGroupMultiple', function(req,resp){
	var userid=req.query.userid
	delete req.query.userid
	var optionSelected=""
	for(var key in req.query){
		optionSelected+=req.query[key]+" "
	}
	// python execution
	var pypath = './process_message/setGroupMultiple.py'
	var options = {mode:'text',args:[userid,optionSelected]}
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

//workout log
app.get('/workoutLog', function(req, resp){
	var userid=req.query.userid
	resp.render('workoutlog',{userid:userid})
})
app.get('/storeLog', function(req, resp){
	var userid=req.query.userid
	// python execution
	var pypath = './process_message/workoutLog.py'
	var options = {mode:'text',args:[JSON.stringify(req.query)]}
	PythonShell.run(pypath,options,function(err,results){
		if(err) throw err
		for(var idx=0; idx<results.length; idx++){
			var messageData=JSON.parse(results[idx])
			console.log("received from python : "+messageData)
			callSendAPI(messageData)
			setTimeout(function(){},1000)
		}
	})

	resp.render('workoutlog',{userid:userid})
})
app.get('/storeLogDone', function(req, resp){
	// python execution
	var pypath = './process_message/workoutLog.py'
	var options = {mode:'text',args:[JSON.stringify(req.query)]}
	PythonShell.run(pypath,options,function(err,results){
		if(err) throw err
		for(var idx=0; idx<results.length; idx++){
			var messageData=JSON.parse(results[idx])
			console.log("received from python : "+messageData)
			callSendAPI(messageData)
			setTimeout(function(){},1000)
		}
	})

	resp.redirect(windowCloseUrl)
})

//statistics
app.get('/progressStats', function(req, resp){
	var userid=req.query.userid
	// python execution
	var pypath = './process_message/exerciseNames.py'
	var options = {mode:'text',args:[userid]}
	PythonShell.run(pypath,options,function(err,results){
		if(err) throw err
		for(var idx=0; idx<results.length; idx++){
			var messageData=results[idx]
			messageData=messageData.replace(/'/g,'"')
			messageData=JSON.parse(messageData)
			//console.log(messageData)
			if(messageData.length > 0)
				resp.render('progressStats',{userid:userid, options:messageData})
			else
				resp.send('No data found! Try Again...')
		}
	})
})
app.get('/getGraph', function(req, resp){
	var userid=req.query.userid
	var exercisename=req.query.exercisename
	//console.log(req.query)
	//python execution
	var pypath = './process_message/exerciseStats.py'
	var options = {mode:'text',args:[JSON.stringify(req.query)]}
	PythonShell.run(pypath,options,function(err,results){
		if(err) throw err
		for(var idx=0; idx<results.length; idx++){
			var messageData=results[idx]
			messageData=messageData.replace(/'/g,'"')
			messageData=JSON.parse(messageData)
			//console.log(messageData)
			if(messageData.length > 0)
				resp.render('viewGraph', {userid:userid, exercisename:exercisename,options:messageData})
			else
				resp.send('No data found! Try Again...')
		}
	})
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