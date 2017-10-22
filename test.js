const PythonShell = require('python-shell');
event={id:123,msg:{text:"hii"}}
var pypath = './msgNlp/sample.py'
var options = {mode:'text',args:[JSON.stringify(event)]}
PythonShell.run(pypath,options,function(err,results){
    if(err) throw err
    var myData=results[0]
    var messageData=results[1]
    var resp=JSON.parse(messageData)
    console.log(myData)
    console.log(typeof(resp.message.text))
})
/*message event sample
event={
    "sender":{ "id":"1250200895092053" },
    "recipient":{"id":"1516761118369603"},
    "timestamp":1508668396423,
    "message":
        {
            "mid":"mid.$cAAU5j9X9Z2RldOobh1fQ6TUYE2yZ",
            "seq":84334,
            "text":"HEY",
            "nlp":{"entities":{}}
        }
}
*/