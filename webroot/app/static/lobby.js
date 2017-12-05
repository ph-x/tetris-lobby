//////////////////
// socket

var socket = io.connect("ws://localhost:8080/lobby_event");

// update player list
socket.on("player_list", function (data){
    data = JSON.parse(data);
    var players = data;

    // remove current player list
    var player_list = document.getElementById("players");
    while(player_list.hasChildNodes())
    {  
        player_list.removeChild(player_list.firstChild);  
    } 

    // append new player list
    for(var i = 0; i < players.length; i++){
        var player_info = document.createElement("LI");
        var textnode = document.createTextNode(players[i]);
        player_info.appendChild(textnode);
    	player_list.appendChild(player_info);
    }
});

// update room list
socket.on("room_list", function (data){
    data = JSON.parse(data);
    var rooms = data;
    // remove current room list
    var room_list = document.getElementById("rooms");
    while(room_list.hasChildNodes())
    {  
        room_list.removeChild(room_list.firstChild);  
    } 

    // append new room list
    room_id_list = new Array();
    for(var i = 0; i < rooms.length; i++){
        // record match id in array
        room_id_list[i] = rooms[i]['match_id'];

        // create DOM elements and append it to html

        var room_info = document.createElement("LI");
        var room_button = document.createElement("BUTTON");
        room_button.type = "button";
        room_button.className = "room_button";

        var player1_info = rooms[i]['player1'];
        if (player1_info == null) {
            player1_info = "\0";
        }
        var player2_info = rooms[i]['player2'];
        if (player2_info == null) {
            player2_info = "\0";
        }
        var player1_node = document.createElement("P");
        //player1_node.innerHTML = player1_info;
        var textnode = document.createTextNode(player1_info);
        player1_node.appendChild(textnode);
        var player2_node = document.createElement("P");
        //player2_node.innerHTML = player2_info;
        textnode = document.createTextNode(player2_info);
        player2_node.appendChild(textnode);

        room_button.appendChild(player1_node);
        room_button.appendChild(player2_node);
        room_info.appendChild(room_button);
        room_list.appendChild(room_info);
    }

    // bind onclick events on buttons
    var room_buttons = document.getElementsByClassName("room_button");
    for(var i = 0; i < room_buttons.length; i++){
        room_buttons[i].setAttribute("i", i);
        room_buttons[i].onclick = function(){
            var index = this.getAttribute("i");
            window.location.href = "/match/" + room_id_list[index];
        };
    }
});

// chat msg received
socket.on("chat_msg", function (data){
	data = JSON.parse(data);
    var player = data['player'];
    var msg = data['message'];
    var textnode; 

    // make a LI element
    var msg_node = document.createElement("LI");

    var player_info = document.createElement("P");
    player_info.className = "player";
    //player_info.innerHTML = player + ":";
    textnode = document.createTextNode(player + ":");
    player_info.appendChild(textnode);

    var msg_info = document.createElement("P");
    msg_info.className = "content";
    //msg_info.innerHTML = msg;
    textnode = document.createTextNode(msg);
    msg_info.appendChild(textnode);

    msg_node.appendChild(player_info);
    msg_node.appendChild(msg_info);

    // append element to the chat area
    document.getElementById("chat-msgs").appendChild(msg_node);

    //scroll chat area to bottom
    var chat_area = document.getElementById("chat-msgs");
    console.log("off " + chat_area.scrollHeight);
    console.log("clientH " + chat_area.clientHeight);
    chat_area.scrollTop = chat_area.scrollHeight - chat_area.clientHeight;
    
});

// create response
socket.on("create_res", function (data){
    data = JSON.parse(data);
    window.location.href = "/match/" + data['match_id'];
});

//////////////////
// lobby 

var room_id_list = new Array();

// create a room
document.getElementById("newroom_btn").onclick = function(){
    socket.emit("create");
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
    socket.emit("chat_msg", {"message": chat_msg});
};


