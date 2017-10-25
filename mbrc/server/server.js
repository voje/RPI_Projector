const express = require('express')
const fs = require('fs')

const app = express()
const port = 3345
//const filepath = "test.txt" // TODO write to fifo

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
    var html = fs.readFileSync('./public/index.html', 'utf8')
    res.send(html)
})

app.get('/command', function(req, res) {
    var k = req.query.key
    k1 = map[k]
    if (typeof(k1) == 'undefined') {
        k1 = k  //use the default input
    }
    console.log(k1) //TODO: write to file
    res.send("ello")
    //&rarr;
})

app.listen(port, function () {
    console.log('Example app listening on port '+port+'!')
})
