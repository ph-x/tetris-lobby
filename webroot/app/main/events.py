import json
from app import tetris_logic
from flask import request
from flask_socketio import join_room
from .. import socketio


# insecure, require user authentication
@socketio.on('join', namespace='/game')
def on_join(data):
    print(request.sid, "join")
    sid = request.sid
    room = data['room']
    join_room(room)
    current_player = tetris_logic.Player(sid)
    current_player.opponent = None
    for psid in tetris_logic.Shared.players:
        current_player.opponent = tetris_logic.Shared.players[psid]
        tetris_logic.Shared.players[psid].opponent = current_player
    tetris_logic.Shared.players[sid] = current_player


# need to leave room when room structure is avaliable
@socketio.on('leave', namespace='/game')
def on_leave():
    print(request.sid, 'leave')
    if request.sid in tetris_logic.Shared.game:
        tetris_logic.Shared.game[request.sid].stop_game()
    if request.sid in tetris_logic.Shared.players:
        del tetris_logic.Shared.players[request.sid]


@socketio.on('disconnect', namespace='/game')
def test_disconnect():
    on_leave()


def start_game():
    print('start')
    game = {}
    tetris_logic.Shared.game_status = 'on'
    tetris_logic.Shared.loser = None
    tetris_logic.Shared.game = game
    for psid in tetris_logic.Shared.players:
        game[psid] = tetris_logic.Tetris(psid)
    socketio.emit('game_status', json.dumps({'action': 'start'}), namespace='/game')


# insecure, require user authentication
@socketio.on('ready', namespace='/game')
def on_ready(data):
    if tetris_logic.Shared.game_status is 'on':
        return
    print(request.sid)
    for psid in tetris_logic.Shared.players:
        player = tetris_logic.Shared.players[psid]
        if psid is request.sid:
            player.ready()
            print(player.is_ready)
            if player.opponent is not None and player.opponent.is_ready:
                start_game()


@socketio.on('operate', namespace='/game')
def operate_game(instruction):
    game = tetris_logic.Shared.game
    if len(game) and request.sid in game.keys():
        game[request.sid].operate(instruction=instruction)
