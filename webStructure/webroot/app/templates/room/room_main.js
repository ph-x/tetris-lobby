$.(function(){
	var socket = io();

	// select all variables
	var $opponent = $(".opponent");
	var $ready_button = $(".game-ready");
	var $chat_box = $(".chat-box");
	var $chat_submit = $(".chat-submit");

	// configs
	var opponent_in = "opponent_in";
	var opponent_out = "opponent_out";
	var ready = "game ready";
	var ready_cancel = "ready canceled";

	var game_start = "game_start";
	var game_over = "game_over";

	/////////////////////
	// game rendering 
	/////////////////////
	var game = new Phaser.Game(800, 600, Phaser.AUTO, 'game-area', { preload: preload, create: create, update: update });

	function preload() {
	    // load assets
	}

	function create() {
		// construct game stages
	}

	function update() {
		// frame
	}


	/////////////////////
	// socketio part
	/////////////////////
	socket.on("connect", function(data){
		//pass
	});

	socket.on(opponent_in, function(data){
		//opponent_in(data);
	});

	socket.on(opponent_out, function(data){
		//opponent_out(data);
	});

	socket.on(new_msg, function(data){
		//add_msg(data);
	});

	socket.on(game_start, function(data){
		//init_game(data);
	});

	socket.on(game_over, function(data){
		//end_game(data);
	});

	$chat_submit.click(function(){
		//change_ready_state();
	});

	$chat_submit.click(function(){
		//submit_msg();
	});
})