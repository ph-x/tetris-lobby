//////////////////
// socket

var socket = io.connect("ws://127.0.0.1:8080/lobby");

// when connected, request user info (I'd prefer server send it without request)
socket.on("connect", function (){
	socket.emit("user_info");
});

// get user_info
socket.on("user_info", function (data){
    data = JSON.parse(data);
    var user = data['user'];
    //show user name on the block
});

// update player list
socket.on("player_list", function (data){
    data = JSON.parse(data);
    var players = data['player_list'];
    // remove current player list
    // append new player list
});

// update room list
socket.on("room_list", function (data){
    data = JSON.parse(data);
    var rooms = data['room_list'];
    // remove current room list
    // append new room list
});

//////////////////
// lobby 

var room_list;

// create a room
document.getElementById("newroom_btn").onclick = function(){
    // debug
    socket.emit("create_room", {});
};

// join a room
document.getElementById("newroom_btn").onclick = function(){
    // debug
    socket.emit("create_room", {});
};

//chat input hotkey (enter)
document.getElementById("chat-box").firstElementChild.onkeydown = function(e){
    if (e.keyCode == 13) {
        document.getElementById("chat-submit").click();
    }
};

// chat submit button
document.getElementById("chat-submit").onclick = function(){

    var input_box = document.getElementById("chat-box").firstElementChild;
    var chat_msg = input_box.value;
    if(chat_msg == ""){
        return;
    }
    input_box.value = "";
    console.log(chat_msg);
    socket.emit("chat_msg", chat_msg);
};

