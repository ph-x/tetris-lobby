var socket = io.connect("127.0.0.1:5000/game");

var startButton = document.getElementById("start");
startButton.onclick = function () {
    socket.emit("start");
};

$(document).keydown(function(e) {
    if (event.defaultPrevented) {
    return;                         // do nothing if the event was already processed
    }
    var instruction;
    switch(e.key) {
        case "ArrowLeft":
        instruction = "left"; break;

        case "ArrowUp":
        instruction = "up"; break;

        case "ArrowRight":
        instruction = "right"; break;

        case "ArrowDown":
        instruction = "down"; break;

        default: return;            // exit this handler for other keys
    }
    socket.emit("operate", instruction);
    e.preventDefault();             // prevent the default action (scroll / move caret)
});


socket.on('game', function (data) {
    var matrix = data.split(",");

    var message = "";               //width and height are hard coded here
    for (var i=0; i < 10; i++){
        for (var j=0; j < 10; j++){
            message += matrix.shift();
        }
        message += "<br>";
    }
    document.getElementById("message").innerHTML = message;
});


socket.on('gameover', function (data) {
    document.getElementById("message").innerHTML = data;
})