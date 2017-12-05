import threading
from flask_socketio import join_room, leave_room
from app.main import main
from flask import send_from_directory, render_template, request
from flask_login import current_user
from .. import socketio
import json

match_lock = threading.Lock()  # guards the following 2 data structures
sid_match = {}  # sid -> match_id
match_players = {}  # match_id -> Match

reserved_rooms = ['lobby_chat']
reserved_rooms = {x: i for i, x in enumerate(reserved_rooms)}

id_lock = threading.Lock()  # guards the match id
next_match = len(reserved_rooms)


class JoinFailureError(Exception):
    pass


class MatchError(Exception):
    pass


class Match:
    def __init__(self, player1=None, player2=None):
        self.player1 = player1
        self.player2 = player2

    def add(self, username):
        if username in self:
            return
        if self.player1 is None:
            self.player1 = username
        elif self.player2 is None:
            self.player2 = username
        else:
            raise MatchError('match is full')

    def remove(self, username):
        if self.player1 == username:
            self.player1 = None
        elif self.player2 == username:
            self.player2 = None
        else:
            raise MatchError('{} is not a player in this match'.format(username))

    def is_empty(self):
        return self.player1 is None and self.player2 is None

    def is_full(self):
        return self.player1 is not None and self.player2 is not None

    def __contains__(self, username):
        return self.player1 == username or self.player2 == username

    def __repr__(self):
        return 'Player({}, {})'.format(self.player1, self.player2)


def alloc_match_id():
    global next_match
    with id_lock:
        match_id = next_match
        next_match += 1
    return match_id


@main.route('/match/<match_id>')
def get_match(match_id):
    return render_template('room.html')


@main.route('/lobby')
def get_lobby():
    return render_template('lobby.html')


def join_match(match_id, sid):
    with match_lock:
        try:
            match = match_players[match_id]
        except KeyError:
            # create new match or reject
            with id_lock:
                highest_id = next_match
            if match_id >= highest_id:
                # reject
                print('rejecting create room {}!'.format(match_id))
                raise JoinFailureError(
                    'user {} wants to join nonexistent match {}'.format(sid, match_id))
            else:
                # create a match
                print('reusing room id {}'.format(match_id))
                join_room(match_id, sid)  # todo: can be lifted out of locked region
                sid_match[sid] = match_id
                match_players[match_id].add(current_user.username)
        else:
            # join match normally
            print('joining match {}!'.format(match_id))
            if match.is_full():
                raise JoinFailureError('match {} is full'.format(match_id))
            join_room(match_id, sid)  # todo: can be lifted out of locked region
            sid_match[sid] = match_id
            data = [{'player1': v.player1,
                     'player2': v.player2,
                     'match_id': k}
                    for k, v in match_players.items()]
            print(sid_match)
            print(match_players)
            socketio.emit('room_list',
                          json.dumps(data),
                          namespace='/lobby_event',
                          room=request.sid)


def leave_match(sid):
    with match_lock:
        try:
            match_id = sid_match[sid]  # leave match if in one
        except KeyError:
            print('session {} not leaving room!'.format(sid))
            pass  # do nothing if not in a match
        else:
            print('session {} leaving room {}!'.format(sid, match_id))
            del sid_match[sid]
            leave_room(match_id, sid)  # todo: can be lifted out of locked region
            match_players[match_id].remove(current_user.username)
            if match_players[match_id].is_empty():
                # destroy the match if empty
                del match_players[match_id]
            data = [{'player1': v.player1,
                     'player2': v.player2,
                     'match_id': k}
                    for k, v in match_players.items()]
            print(sid_match)
            print(match_players)
            socketio.emit('room_list',
                          json.dumps(data),
                          namespace='/lobby_event',
                          room=request.sid)


def all_matches():
    return match_players.keys()


def all_waiting_matches():
    return [k for k, v in match_players.items() if not v.is_full()]


def match_for(sid):
    with match_lock:
        return sid_match[sid]


@socketio.on('create', namespace='/lobby_event')
def on_create():
    match_id = alloc_match_id()
    print('new match id {} allocated'.format(match_id))
    socketio.emit('create_res',
                  json.dumps({'match_id': match_id}),
                  namespace='/lobby_event',
                  room=request.sid)
