"use strict";

var test;

// Add event listeners
let submitButton = document.getElementById("submit");
if (submitButton.addEventListener) {
    submitButton.addEventListener("click", getEvents);
} else if (submitButton.attachEvent) {  // IE8 and earlier
    submitButton.attachEvent("onclick", getEvents);
} // end if -- submitButton click


// Event handler callback functions
function getEvents(evt) {
    /* Sends request for events to server. */

    evt.preventDefault();

    // Make payload
    // This seems much cleaner in jQuery; I might be doing it wrong
    let payload = "start=" + document.getElementsByName("start")[0].value +
                  "&end=" + document.getElementsByName("end")[0].value +
                  "&kind=" + document.getElementsByName("kind")[0].value;

    // Get response message area ready
    let debugEl = document.getElementById("debug");
    debugEl.style.display = "inline-block";
    // debugEl.insertAdjacentText("beforeend", "payload: " + payload);

    // Send to server
    let xhttp = new XMLHttpRequest();
    xhttp.open("GET", '/api?' + payload, true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.onload = function () {
        if ( this.readyState == 4 && this.status == 200 ) {
            let results = JSON.parse(this.responseText);
            updateDensities(results['count'], results['events']);
            // updateMap();
            map.setPaintProperty('us-states',
                                 'fill-color', {
                                    property: 'density',
                                    stops: [
                                        [0, '#70F1FF'],
                                        [10, '#56D7FF'],
                                        [20, '#3DBEFF'],
                                        [50, '#23A4FF'],
                                        [100, '#0A8BE6'],
                                        [200, '#0071CC'],
                                        [500, '#0058B3'],
                                        [1000, '#003E99']
                                    ]
                                }); //,
                                // 'fill-opacity': 0.75);

        } else {
            debugEl.insertAdjacentHTML("beforeend",
                                       "<p>" + this.responseText + "</p>");
        } // end if
    };
    xhttp.send();

} // end getEvents


function pyGet(object, key, default_value) {
    /* Faking a Python dictionary .get() method thanks to:
       https://stackoverflow.com/a/44185289

       Use it like:
          var obj = {"a": 1};
          get(obj, "a", 2); // -> 1
          get(obj, "b", 2); // -> 2

    */

    let result = object[key];
    return (typeof result !== "undefined") ? result : default_value;
}
