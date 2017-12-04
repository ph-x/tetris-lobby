import json
import lobby
from app import tetris_logic
from flask import request
from flask_socketio import join_room, rooms
from flask_login import current_user
from .. import socketio

#a match is equavilent to a room

#no conflict exist, no need for lock
#match_id -> RoomInfo
match_rminfo = {}
@socketio.on('join', namespace='/game')
def prepare_game(data):
    #create new room when
    room_id = data['room']
    join_room(room_id)
    if room_id not in match_rminfo:
        match_rminfo[room_id] = tetris_logic.RoomInfo(room_id)
        room_info = match_rminfo[room_id]
    sid = request.sid
    current_player = tetris_logic.Player(sid=sid, username=current_user.username)
    current_player.opponent = None
    for psid in room_info.players:
        current_player.opponent = room_info.players[psid]
        room_info.players[psid].opponent = current_player
    room_info.players[sid] = current_player

@socketio.on('leave', namespace='/game')
def leave_game():
    username = current_user.username
    try:
        room_id = lobby.uid_match[username]
        room_info = match_rminfo[room_id]
    except KeyError:
        raise RuntimeError('user {} is not in a game'.format(username))
    if room_info.game_status is 'on':
        room_info.game[request.sid].stop_game()
    if request.sid in room_info.players:
        del room_info.players[request.sid]


@socketio.on('disconnect', namespace='/game')
def on_disconnect():
    leave_game()

@socketio.on('chat', namespace='/game')
def chat(data):
    room_list = rooms()
    for room in room_list:
        socketio.emit('chat', data, room=room, namespace='/game')

def start_game(room_id):
    try:
        room_info = match_rminfo[room_id]
    except KeyError:
        raise RuntimeError('room {} does not exist'.format(room_id))
    game = {}
    #init room
    room_info.game_status = 'on'
    room_info.loser = None
    room_info.game = game
    #start games
    for psid in room_info.players:
        game[psid] = tetris_logic.Tetris(sid=psid, room_info=room_info)
    socketio.emit('game_status', json.dumps({'action': 'start'}), namespace='/game')


# insecure, require user authentication
@socketio.on('ready', namespace='/game')
def on_ready(data):
    try:
        room_id = lobby.uid_match[current_user.username]
        room_info = match_rminfo[room_id]
    except KeyError:
        raise RuntimeError('user {} is not in a room'.format(username))
    #block ready message when game is on
    if room_info.game_status is 'on':
        return
    if request.sid in room_info.players:
        player = room_info.players[request.sid]
        player.ready()
        print(player.is_ready)
        if player.opponent is not None and player.opponent.is_ready:
            start_game(room_id)

@socketio.on('operate', namespace='/game')
def operate_game(instruction):
    try:
        room_id = lobby.uid_match[current_user.username]
        room_info = match_rminfo[room_id]
    except KeyError:
        raise RuntimeError('user {} is not in a room'.format(username))
    game = room_info.game
    if len(game) and request.sid in game.keys():
        game[request.sid].operate(instruction=instruction)
