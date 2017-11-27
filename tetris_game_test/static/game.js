//////////////////
// config

var config = {
    "key_sensitivity" : 4
}


//////////////////
// socket

var socket = io.connect("localhost:5000");

var game_bitmap;
var next;
var next_next;

socket.on("update", function (data){
    data = JSON.parse(data);
    game_bitmap = data['game_bitmap'];
    next = data['next'];

    draw_game();
});


//////////////////
// game

var game_height = 528;
var game_width = 240;

var game = new Phaser.Game(game_width, game_height, Phaser.AUTO, '', { preload: preload, create: create, update: update });

var cursors;
var block_group;

function preload() {

    game.load.image('background', 'static/assets/background.png');
    game.load.spritesheet('block', 'static/assets/block.png', 24, 24);

}

function create() {

    // draw UI
    game.add.image(0, 0, 'background');
    //game.add.sprite(30, 30, 'game_area');
    //game.add.sprite(600, 50, "next_area");

    block_group = game.add.group();

    // create controller
    cursors = game.input.keyboard.createCursorKeys();

}

var key_cumulate = 0;
function update() {

    // send control to server
    if (cursors.left.isDown)
    {
        key_cumulate++;
        if(key_cumulate > config.key_sensitivity){
            key_cumulate -= config.key_sensitivity;
            socket.emit("control", "left");
        }
    }
    else if (cursors.right.isDown)
    {
        key_cumulate++;
        if(key_cumulate > config.key_sensitivity){
            key_cumulate -= config.key_sensitivity;
            socket.emit("control", "right");
        }
    }
    else if (cursors.up.isDown)
    {
        key_cumulate++;
        if(key_cumulate > config.key_sensitivity){
            key_cumulate -= config.key_sensitivity;
            socket.emit("control", "up");
        }
    }
    else if (cursors.down.isDown)
    {
        key_cumulate++;
        if(key_cumulate > config.key_sensitivity){
            key_cumulate -= config.key_sensitivity;
            socket.emit("control", "down");
        }
    }

}

function draw_game() {

    block_group.destroy();
    block_group = game.add.group();
    // draw bitmap and nxt 
    render_blocks(game_bitmap, 0, 0);
    //render_blocks(next, 600, 50);

}

function render_blocks(blocks, x, y){

    if (typeof(blocks) == undefined){
        return;
    }
    for(var i = 0; i < blocks.length; i++){
        for(var j = 0; j < blocks[i].length; j++){
            if(blocks[i][j] != 0){
                block_group.create(x+j*24, y+i*24, 'block');
            }
        }
    }

}
