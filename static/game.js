//////////////////
// config

var config = {
    "key_sensitivity"       : 4,
    "key_up_delay"          : 200,
    "key_down_delay"        : 100,
    "key_left_delay"        : 50,
    "key_right_delay"       : 50,
    "block_height"          : 24,
    "block_width"           : 24,
    "block_image_height"    : 96,
    "block_image_width"     : 96
}


//////////////////
// socket

var socket = io.connect("localhost:5000/game");

socket.emit("join", {"room" : 0});

var game_bitmap;

socket.on("game_msg", function (data){
    var game;
    data = JSON.parse(data);
    game_bitmap = data['bitmap'];
    var player = data['player'];

    if(player == "left"){
        game = game1;
    }
    else if(player == "right"){
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
        socket.emit("operate", "left");
    });
    cursors.right.onDown.add(function(){
        socket.emit("operate", "right");
    });
    cursors.up.onDown.add(function(){
        socket.emit("operate", "up");
    });
    cursors.down.onDown.add(function(){
        socket.emit("operate", "down");
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
                socket.emit("operate", "left");
            }
        }
    }
    else if (cursors.right.isDown)
    {
        if(cursors.right.duration > config.key_right_delay){
            key_cumulate++;
            if(key_cumulate > config.key_sensitivity){
                key_cumulate -= config.key_sensitivity;
                socket.emit("operate", "right");
            }
        }
    }
    else if (cursors.up.isDown)
    {
        if(cursors.up.duration > config.key_up_delay){
            key_cumulate++;
            if(key_cumulate > config.key_sensitivity){
                key_cumulate -= config.key_sensitivity;
                socket.emit("operate", "up");
            }
        }
    }
    else if (cursors.down.isDown)
    {
        if(cursors.down.duration > config.key_down_delay){
            key_cumulate++;
            if(key_cumulate > config.key_sensitivity){
                key_cumulate -= config.key_sensitivity;
                socket.emit("operate", "down");
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
