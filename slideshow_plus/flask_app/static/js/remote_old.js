var focused;
var saved_classes; //when a button loses focus, it gets its old classes
var prevr;
var prev1;

window.onload = function () {
    var i, keys = document.getElementsByClassName("key");
    for (i = 0; i < keys.length; i += 1) {
        keys[i].onclick = clickHandler;
    }
    prevl = document.getElementById("prev-l");
    prevl.innerText = "";
    prevr = document.getElementById("prev-r");
    prevr.innerText = "";
    body = document.getElementByTagName("body")
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
                prevl.innerText += focused.innerText;
            } else {
                prevl.innerText = "" ;
            }
        } else {
            //prev.innerText = "Napaka 1"
        }
        //TODO: json parser complaining
        var response = JSON.parse(this.responseText);
        if (!response["success"]) {
            body.className = "red-bg";
            return;
        }
        prevr.innerText = response["current_file"]["filename"];
        if (!response["blank"] && response["projector_state"] == "on") {
            prevr.className = "green-text"
        } else {
            prevr.className = "";
        }
    }
    xhttp.open("GET", url, true);
    xhttp.send();
}