//////////////////
// config

var config = {
    "key_sensitivity"       : 4,
    "key_up_delay"          : 200,
    "key_down_delay"        : 100,
    "key_left_delay"        : 100,
    "key_right_delay"       : 100,
    "block_height"          : 24,
    "block_width"           : 24,
    "block_image_height"    : 96,
    "block_image_width"     : 96
};


//////////////////
// socket

var socket = io.connect("127.0.0.1:8080/game");

// room_id is the last part of URL: room_id == window.location.search
var the_room_id = window.location.pathname.split("/")[1];
console.log("room_id is " + the_room_id);
socket.emit("join", {"room" : the_room_id});

// cannot join room
socket.on("join_failure", function (data){
    data = JSON.parse(data);
    var err_msg = data['err_msg'];
    alert(err_msg);
    // a static url, need to be modified if url changed in server side
    window.location.href = "/lobby";
});

// game_status: 0 -- end, 1 -- start
var game_status = 0;
var game_bitmap;

socket.on("game_msg", function (data){
    var game;
    data = JSON.parse(data);
    game_bitmap = data['bitmap'];
    var player = data['player'];

    if(player == "self"){
        game = game1;
    }
    else if(player == "other"){
        game = game2;
    }
    draw_game(game);
});

socket.on("game_status", function (data){
    data = JSON.parse(data);
    var game_action = data['action'];

    if(game_action == "start"){
        game_status = 1;

        regames();
    }
    else if(game_action == "end"){
        game_status = 0;

        block_group1.alpha = 0.3;
        block_group2.alpha = 0.3;

        var loser = data['loser'];
        if(loser == "self"){
            draw_message(game1, "You Lose!");
            draw_message(game2, "Win!");
        }
        else if(loser == "other"){
            draw_message(game1, "You Win!");
            draw_message(game2, "Lose!");
        }
    }
});

//////////////////
// room

// ready button
document.getElementById("game-ready").onclick = function(){
    socket.emit("ready");
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
    socket.emit("chat_msg", {"message": chat_msg});
};

// chat msg received
socket.on("chat_msg", function (data){
    data = JSON.parse(data);
    var players = data['player'];
    var msg = data['message'];

    // make a LI element
    var msg_node = document.createElement("LI");

    var player_info = document.createElement("P");
    player_info.class = "player";
    player_info.innterHTML = msg + ":";

    var msg_info = document.createElement("P");
    msg_info.class = "content";
    msg_info.innterHTML = msg;

    msg_node.appendChild(player_info);
    msg_node.appendChild(msg_info);

    // append element to the chat area
    document.getElementById("chat-msgs").appendChild(msg_node);

});

// player updated
socket.on("player_update", function (data){
    data = JSON.parse(data);
    var player1_info = data['player1'];
    var player2_info = data['player2'];
    if (player2_info == 0){
        player2_info = "None";
    }

    // remove elements from info area
    document.getElementById("user-info-1").removeChild(document.getElementById("user-info-1").firstChild);
    document.getElementById("user-info-2").removeChild(document.getElementById("user-info-2").firstChild);

    // make P elements
    var player1_node = document.createElement("P");
    var player2_node = document.createElement("P");
    player1_node.innterHTML = player1_info;
    player2_node.innterHTML = player2_info;

    // append elements to info area
    document.getElementById("user-info-1").appendChild(player1_node);
    document.getElementById("user-info-2").appendChild(player2_node);
});

//////////////////
// game renderer

var game_height = 528;
var game_width = 240;

var game1 = new Phaser.Game(game_width, game_height, Phaser.AUTO, document.getElementById("game-l"), { preload: preload1, create: create1, update: update1 }, true);
var game2 = new Phaser.Game(game_width, game_height, Phaser.AUTO, document.getElementById("game-r"), { preload: preload2, create: create2 }, true);

var cursors;
var block_group1;
var block_group2;

function preload1() {

    game1.load.spritesheet('block1', 'static/image/block_1.png', config.block_image_width, config.block_image_height);
    game1.load.spritesheet('block2', 'static/image/block_2.png', config.block_image_width, config.block_image_height);
    game1.load.spritesheet('block3', 'static/image/block_3.png', config.block_image_width, config.block_image_height);
    game1.load.spritesheet('block4', 'static/image/block_4.png', config.block_image_width, config.block_image_height);
    game1.load.spritesheet('block5', 'static/image/block_5.png', config.block_image_width, config.block_image_height);
    game1.load.spritesheet('block6', 'static/image/block_6.png', config.block_image_width, config.block_image_height);
    game1.load.spritesheet('block7', 'static/image/block_7.png', config.block_image_width, config.block_image_height);

}

function preload2() {

    game2.load.spritesheet('block1', 'static/image/block_1.png', config.block_image_width, config.block_image_height);
    game2.load.spritesheet('block2', 'static/image/block_2.png', config.block_image_width, config.block_image_height);
    game2.load.spritesheet('block3', 'static/image/block_3.png', config.block_image_width, config.block_image_height);
    game2.load.spritesheet('block4', 'static/image/block_4.png', config.block_image_width, config.block_image_height);
    game2.load.spritesheet('block5', 'static/image/block_5.png', config.block_image_width, config.block_image_height);
    game2.load.spritesheet('block6', 'static/image/block_6.png', config.block_image_width, config.block_image_height);
    game2.load.spritesheet('block7', 'static/image/block_7.png', config.block_image_width, config.block_image_height);

}

function create1() {

    // draw UI

    block_group1 = game1.add.group();

    // create controller
    cursors = game1.input.keyboard.createCursorKeys();

    // guarantee at least 1 action per operate
    cursors.left.onDown.add(function(){
        socket.emit("operate", {"instrcution": "left"});
    });
    cursors.right.onDown.add(function(){
        socket.emit("operate", {"instrcution": "right"});
    });
    cursors.up.onDown.add(function(){
        socket.emit("operate", {"instrcution": "up"});
    });
    cursors.down.onDown.add(function(){
        socket.emit("operate", {"instrcution": "down"});
    });

    // eliminate key counter when key is up
    cursors.left.onUp.add(function(){
        key_cumulate = 0;
    });
    cursors.right.onUp.add(function(){
        key_cumulate = 0;
    });
    cursors.up.onUp.add(function(){
        key_cumulate = 0;
    });
    cursors.down.onUp.add(function(){
        key_cumulate = 0;
    });

}

function create2() {

    // draw UI

    block_group2 = game2.add.group();

}

var key_cumulate = 0;
function update1() {

    // key hold input

    if (cursors.left.isDown)
    {
        if(cursors.left.duration > config.key_left_delay){
            key_cumulate++;
            if(key_cumulate > config.key_sensitivity){
                key_cumulate -= config.key_sensitivity;
                socket.emit("operate", {"instrcution": "left"});
            }
        }
    }
    else if (cursors.right.isDown)
    {
        if(cursors.right.duration > config.key_right_delay){
            key_cumulate++;
            if(key_cumulate > config.key_sensitivity){
                key_cumulate -= config.key_sensitivity;
                socket.emit("operate", {"instrcution": "right"});
            }
        }
    }
    else if (cursors.up.isDown)
    {
        if(cursors.up.duration > config.key_up_delay){
            key_cumulate++;
            if(key_cumulate > config.key_sensitivity){
                key_cumulate -= config.key_sensitivity;
                socket.emit("operate", {"instrcution": "up"});
            }
        }
    }
    else if (cursors.down.isDown)
    {
        if(cursors.down.duration > config.key_down_delay){
            key_cumulate++;
            if(key_cumulate > config.key_sensitivity){
                key_cumulate -= config.key_sensitivity;
                socket.emit("operate", {"instrcution": "down"});
            }
        }
    }

}

function draw_game(game) {
    var block_group;
    if(game == game1){
        block_group = block_group1;
    }
    else if(game == game2){
        block_group = block_group2;
    }
    block_group.removeAll(true, false);
    // draw bitmap and nxt 
    render_blocks(game_bitmap, block_group, 0, 0);
    //render_blocks(next, 600, 50);

}

function render_blocks(blocks, group, x, y){

    if (typeof(blocks) == undefined){
        return;
    }
    for(var i = 0; i < blocks.length; i++){
        for(var j = 0; j < blocks[i].length; j++){
            var block_type;
            if(blocks[i][j] == 0){
                continue;
            }
            else if(blocks[i][j] == 1){
                block_type = "block1";
            }
            else if(blocks[i][j] == 3){
                block_type = "block2";
            }
            else if(blocks[i][j] == 5){
                block_type = "block3";
            }
            else if(blocks[i][j] == 7){
                block_type = "block4";
            }
            else if(blocks[i][j] == 9){
                block_type = "block5";
            }
            else if(blocks[i][j] == 11){
                block_type = "block6";
            }
            else if(blocks[i][j] == 13){
                block_type = "block7";
            }
            var the_block = group.create(x+j*config.block_width, y+i*config.block_height, block_type);
            the_block.scale.setTo(config.block_width / config.block_image_width, config.block_height / config.block_image_height);
        }
    }

}

function regames() {

    // may cause undefined exception
    game1.world.removeAll(true, false);
    game2.world.removeAll(true, false);

    block_group1 = game1.add.group();
    block_group2 = game2.add.group();

}

function draw_message(game, msg) {

    var bar = game.add.graphics();
    bar.beginFill(0x000000, 0.2);
    bar.drawRect(0, game.height / 3, game.width, game.height / 6);

    // font: Comic Sans MS
    var style = { font: "bold 32px Comic Sans MS", fill: "#fff"};

    text = game.add.text(game.width / 2, game.height * 5 / 12 , msg, style);
    text.anchor.setTo(0.5);
    text.setShadow(3, 3, 'rgba(0,0,0,0.5)', 2);

}
