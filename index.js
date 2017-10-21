'use strict'

const express = require('express')
const bodyParser = require('body-parser')
const request = require('request')

const app = express()
//const token = process.env.FB_VERIFY_TOKEN
//const access = process.env.FB_ACCESS_TOKEN
const myPythonScriptPath = './test/sample.py';

// Use python shell
const PythonShell = require('python-shell');

app.set('port', (process.env.PORT || 5000))

// Allows us to process the data
app.use(bodyParser.urlencoded({extended: false}))
app.use(bodyParser.json())

// ROUTES
app.get('/', function(req, res) {
    const pyshell = new PythonShell(myPythonScriptPath);
    pyshell.on('message', function (message) {
        // received a message sent from the Python script (a simple "print" statement)
        console.log(message);
    });
    
    // end the input stream and allow the process to exit
    pyshell.end(function (err) {
        if (err){
            throw err;
        };
    
        console.log('finished');
    });
	res.send("Hi, I am Darwin your personal health assistant!")
})