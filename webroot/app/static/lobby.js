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
    var user_info = document.createElement("li");
    user_info.innterHTML = user;
    document.getElementById("user-info").appendChild(user_info);
});

// update player list
socket.on("player_list", function (data){
    data = JSON.parse(data);
    var players = data['player_list'];

    // remove current player list
    var player_list = document.getElementById("players");
    while(player_list.hasChildNodes())
    {  
        player_list.removeChild(player_list.firstChild);  
    } 

    // append new player list
    for(var i = 0; i < player_list.length; i++){
        var player_info = document.createElement("li");
    	player_info.innterHTML = players[i];
    	player_list.appendChild(player_info);
    }
});

// update room list
socket.on("room_list", function (data){
    data = JSON.parse(data);
    var rooms = data['room_list'];
    // remove current room list
    // append new room list
});

// chat msg received
socket.on("chat_msg", fucntion (data){
	data = JSON.parse(data);
    var players = data['player'];
    var msg = data['message'];

    // make a LI element
    var msg_node = document.createElement("li");

    var player_info = document.createElement("p");
    player_info.class = "player";
    player_info.innterHTML = msg + ":";

    var msg_info = document.createElement("p");
    msg_info.class = "content";
    msg_info.innterHTML = msg;

    msg_node.appendChild(player_info);
    msg_node.appendChild(msg_info);

    // append element to the chat area
    document.getElementById("chat-msgs").appendChild(msg_node);

});

//////////////////
// lobby 

var room_list;

// create a room
document.getElementById("newroom_btn").onclick = function(){
    // debug
    socket.emit("create_room", {});
};

// TODO: join a room
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


