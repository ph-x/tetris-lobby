$.(function(){
	var socket = io();

	// select all variables
	var $rooms = $(".rooms");
	var $players = $(".players");
	var $chat_msgs = $(".chat-msgs");
	var $chat_box = $(".chat-box");
	var $chat_submit = $(".chat-submit");

	// configs
	var new_player = "new player";
	var new_room = "new room";
	var new_msg = "new msg";

	socket.on("connect", function(data){
		//init_playerlist(data);
		//init_roomlist(data);
	});

	socket.on(new_player, function(data){
		//add_player(data);
	});

	socket.on(new_room, function(data){
		//add_room(data);
	});

	socket.on(new_msg, function(data){
		//add_msg(data);
	});

	$chat_submit.click(function(){
		//submit_msg();
	});
})