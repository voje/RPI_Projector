const express = require('express')
const fs = require('fs')

const app = express()
const port = 3345

const index_path = "./mbrc/public/index.html"
const fifo_path = "./python_script/ir.fifo"

const map = {
    "←": "KEY_VOLUMEDOWN",
    "→": "KEY_VOLUMEUP",
    "↑": "KEY_UP",
    "↓": "KEY_DOWN",
    "On": "KEY_O",
    "Off": "KEY_P",
    "Sleep": "KEY_R",
    "Enter": "KEY_ENTER",
    "Delete": "KEY_DELETE"
}

app.get('/client', function(req, res) {
    var html = fs.readFileSync(index_path, 'utf8')
    res.send(html)
})

app.get('/command', function(req, res) {
    var k = req.query.key
    k1 = map[k]
    if (typeof(k1) == 'undefined') {
        k1 = k  //use the default input
    }
    fs.appendFile(fifo_path, k1+"\n", function(err) {  
	    if (err) throw err
	    console.log("Written to ir.fifo: " + k1)
    })
    res.send("OK")
    //&rarr;
})

app.listen(port, function () {
    console.log('Capture app listening on port '+port+'!')
})
