var socket = io.connect("127.0.0.1:5000/game");

var startButton = document.getElementById("start");
startButton.onclick = function () {
    socket.emit("join",{'room':0})
    socket.emit("ready",{});
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

var matrix1 = null;
var matrix2 = null;
socket.on('game_msg', function (data) {

    var picture1 = data.bitmap;
    matrix1 = picture1.split(",");

    var message = "";               //width and height are hard coded here
    if (matrix1 != null){
      for (var i=0; i < 22; i++){
          for (var j=0; j < 10; j++){
              message += matrix1.shift();
          }
          message += "<br>";
      }
    }
    if (matrix2 != null){
      for (var i=0; i < 22; i++){
          for (var j=0; j < 10; j++){
              message += matrix2.shift();
          }
          message += "<br>";
      }
    }
    document.getElementById("message").innerHTML = message;
});


socket.on('gameover', function (data) {
    document.getElementById("message").innerHTML = data;
})
