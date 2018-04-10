var focused;
var saved_classes; //when a button loses focus, it gets its old classes
var prevr, prevl, body, key_sleep, key_on, key_off;

window.onload = function () {
    var i, keys = document.getElementsByClassName("key");
    for (i = 0; i < keys.length; i += 1) {
        keys[i].onclick = clickHandler;
    }
    prevl = document.getElementById("prev-l");
    prevl.innerText = "";
    prevr = document.getElementById("prev-r");
    prevr.innerText = "";
    body = document.getElementsByTagName("body")[0];
    key_sleep = document.getElementById("key-sleep");
    key_on = document.getElementById("key-on");
    key_off = document.getElementById("key-off");
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

    //update control
    if (!isNaN(txt)) {
        prevl.innerText += txt;
    } else {
        prevl.innerText = "" ;
    }

    //send data
    var xhttp = new XMLHttpRequest();
    var url = "/command?key="+command_map(txt);
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            if (this.status == 200) {
                var response = JSON.parse(this.responseText);
                var current_file = response["current_file"];
                if (current_file != null) {
                    prevr.innerText = response["current_file"]["filename"];
                } else {
                    prevr.innerText = ""
                }
                if (!response["blank"] && response["projector_state"] == "on") {
                    prevr.className = "green-text"
                } else {
                    prevr.className = "";
                }
                body.className = ""; 

		// blank button
                if (!response["blank"] && response["projector_state"] === "on") {
                    key_on.className = "key green-bg"
                } else {
                    key_on.className = "key"
                }

		// on button
                if (response["blank"]) {
                    key_sleep.className = "key green-bg"
                } else {
                    key_sleep.className = "key"
                }

		// of button
		if (response["projector_state"] === "off") {
			key_off.className = "key green-bg"
		} else {
			key_off.className = "key"	
		}
            } else if (this.status == 0) {
                body.className = "red-bg";
            }
        }
    }
    xhttp.open("GET", url, true);
    xhttp.send();
}
