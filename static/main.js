var socket = io.connect("localhost:5000/chat");

function getRoom() {
    var radios = document.getElementsByName('room');
    var roomId;
    for (var i = 0, length = radios.length; i < length; i++) {
        if (radios[i].checked) {
            roomId = radios[i].value;
            return roomId;
        }
    }
}

var joinButton = document.getElementById("join");
joinButton.onclick = function () {
    var username = document.getElementById("username").value;
    var roomId = getRoom();
    var data = {};
    data['username'] = username;
    data['room'] = roomId;
    socket.emit("join", data);
};

var enterButton = document.getElementById("enter");
enterButton.onclick = function send_message() {
    var username = document.getElementById("username").value;
    var message = document.getElementById("message").value;
    var roomId = getRoom();
    var data = {};
    data['username'] = username;
    data['message'] = message;
    data['room'] = roomId;
    socket.emit('chat', data);
};

socket.on('chat', function (data) {
    var username = data['username'];
    var message = data['message'];
    console.log(username + ":" + message);
});