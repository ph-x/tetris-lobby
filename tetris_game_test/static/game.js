//////////////////
// config

var config = {
    "key_sensitivity" : 4
}


//////////////////
// socket

var socket = io.connect("localhost:5000/game");

socket.emit("join", {"room" : 0});

var game_bitmap;

socket.on("game_msg", function (data){
    var game;
    data = JSON.parse(data);
    game_bitmap = data['game_bitmap'];
    player = data['player'];

    if(player == "left"){
        game = game1;
    }
    else(player == "right"){
        game = game2;
    }
    draw_game(game);
});


//////////////////
// room

document.getElementById("game-ready").onclick = function(){
    // debug
    socket.emit("ready", {});
};

//////////////////
// game renderer

var game_height = 528;
var game_width = 240;

var game1 = new Phaser.Game(game_width, game_height, Phaser.AUTO, document.getElementById("game-l"), { preload: preload1, create: create1, update: update_l });
var game2 = new Phaser.Game(game_width, game_height, Phaser.AUTO, document.getElementById("game-r"), { preload: preload2, create: create2 });

var cursors;
var block_group1;
var block_group2;

function preload1() {

    game1.load.image('background', 'static/image/background.png');
    game1.load.spritesheet('block', 'static/image/block.png', 24, 24);

}

function preload2() {

    game2.load.image('background', 'static/image/background.png');
    game2.load.spritesheet('block', 'static/image/block.png', 24, 24);

}

function create1() {

    // draw UI
    game1.add.image(0, 0, 'background');

    block_group1 = game1.add.group();

    // create controller
    cursors = game1.input.keyboard.createCursorKeys();

}

function create2() {

    // draw UI
    game2.add.image(0, 0, 'background');

    block_group2 = game2.add.group();

}

var key_cumulate = 0;
function update1() {

    // send control to server
    if (cursors.left.isDown)
    {
        key_cumulate++;
        if(key_cumulate > config.key_sensitivity){
            key_cumulate -= config.key_sensitivity;
            socket.emit("operate", "left");
        }
    }
    else if (cursors.right.isDown)
    {
        key_cumulate++;
        if(key_cumulate > config.key_sensitivity){
            key_cumulate -= config.key_sensitivity;
            socket.emit("operate", "right");
        }
    }
    else if (cursors.up.isDown)
    {
        key_cumulate++;
        if(key_cumulate > config.key_sensitivity){
            key_cumulate -= config.key_sensitivity;
            socket.emit("operate", "up");
        }
    }
    else if (cursors.down.isDown)
    {
        key_cumulate++;
        if(key_cumulate > config.key_sensitivity){
            key_cumulate -= config.key_sensitivity;
            socket.emit("operate", "down");
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
    block_group.destroy();
    block_group = game.add.group();
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
            if(blocks[i][j] != 0){
                group.create(x+j*24, y+i*24, 'block');
            }
        }
    }

}
