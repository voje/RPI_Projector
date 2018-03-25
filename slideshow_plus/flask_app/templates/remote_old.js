var focused;
var saved_classes; //when a button loses focus, it gets its old classes
var prev;
var prev1;
var prevList = [];

window.onload = function () {
    var i, keys = document.getElementsByClassName("key");
    for (i = 0; i < keys.length; i += 1) {
        keys[i].onclick = clickHandler;
    }
    prev = document.getElementById("prev");
    prev1 = document.getElementById("prev1");
    prev.innerText = "";
    prev1.innerText = "";
};

function command_map(text) {
    var map = {
        "←": "KEY_VOLUMEDOWN",
        "→": "KEY_VOLUMEUP",
        "↑": "KEY_UP",
        "↓": "KEY_DOWN",
        "On": "KEY_O",
        "Off": "KEY_P",
        "Sleep": "KEY_R",
        "Enter": "KEY_ENTER",
        "Delete": "KEY_DELETE"
    };
    if (text in map) {
        return map[text];
    } else {
        return text;
    }
}

function clickHandler(e) {
    if (focused != null) {
        focused.className = saved_classes;
    }
    focused = e.target;
    saved_classes = focused.className;
    focused.className = "key focused";
    var txt = focused.innerText;
    //alert(txt)

    //send data
    var xhttp = new XMLHttpRequest();
    var url = "/command?key="+command_map(txt);
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            //document.getElementById("demo").innerHTML = xhttp.responseText;

            //update control
            if (!isNaN(txt)) {
                prev.innerText += focused.innerText
            } else if (txt == "Enter" && prev.innerText != "") {
                prevList.push(prev.innerText)
                prev1.innerText = prevList[prevList.length-1]
                prev.innerText = "" 
            } else if (txt == "Delete") {
                prevList.splice(-1,1)
                if (prevList.length > 0) {
                    prev1.innerText = prevList[prevList.length-1]
                } else {
                    prev1.innerText = ""
                }
            }
        } else {
            //prev.innerText = "Napaka 1"
        }
        //TODO: json parser complaining
        var response = JSON.parse(this.responseText);
        prev1.innerText = response["current_file"]["filename"];
    }
    xhttp.open("GET", url, true);
    xhttp.send();
}