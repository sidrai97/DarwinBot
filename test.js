const PythonShell = require('python-shell');
event={id:123,msg:{text:"hii"}}
var pypath = './msgNlp/sample.py'
var options = {mode:'text',args:[JSON.stringify(event)]}
PythonShell.run(pypath,options,function(err,results){
    if(err) throw err
    myData=results[0]
    messageData=results[1]
    resp=JSON.parse(messageData)
    console.log(myData)
    console.log(typeof(resp.message.text))
})