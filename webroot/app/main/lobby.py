import threading
from flask_socketio import join_room, leave_room
from app.main import main
from flask_login import current_user
from flask import send_from_directory, redirect, render_template

match_lock = threading.Lock()  # guards the following 2 data structures
uid_match = {}  # uid -> match_id
match_players = {}  # match_id -> Match

reserved_rooms = {'lobby_chat': 0}  # todo: automatic enumerate

id_lock = threading.Lock()  # guards the match id
next_match = len(reserved_rooms)


class Match:
    def __init__(self, player1=None, player2=None):
        self.player1 = player1
        self.player2 = player2

    def add(self, uid):
        if uid in self:
            return
        if self.player1 is None:
            self.player1 = uid
        elif self.player2 is None:
            self.player2 = uid
        else:
            raise RuntimeError('match is full')

    def remove(self, uid):
        if self.player1 == uid:
            self.player1 = None
        elif self.player2 == uid:
            self.player2 = None
        else:
            raise RuntimeError('{} is not a player in this match'.format(uid))

    def is_empty(self):
        return self.player1 is None and self.player2 is None

    def is_full(self):
        return self.player1 is not None and self.player2 is not None

    def __contains__(self, uid):
        return self.player1 == uid or self.player2 == uid


@main.route('/new_match', methods=['GET'])
def new_match():
    global next_match
    with id_lock:
        match_id = next_match
        next_match += 1
        match_players[match_id] = Match(player1=current_user.id)
    return redirect('/match/{}'.format(match_id))


@main.route('/match/<match_id>')
def get_match(match_id):
    uid = current_user.id
    with match_lock:
        try:
            match = match_players[match_id]
        except KeyError:
            raise RuntimeError(
                'user {} wants to join nonexistent match {}'.format(uid, match_id))
        else:
            if match.is_full():
                raise RuntimeError('match {} is full'.format(match_id))
            uid_match[uid] = match_id
            match_players[match_id].add(uid)
    return send_from_directory('static', 'room.html')


@main.route('/lobby')
def get_lobby():
    return render_template('lobby.html')


def join_match(match_id):  # todo: change
    uid = current_user.id
    with match_lock:
        try:
            match = match_players[match_id]
        except KeyError:
            raise RuntimeError(
                'user {} wants to join nonexistent match {}'.format(uid, match_id))
        else:
            if match.is_full():
                raise RuntimeError('match {} is full'.format(match_id))
            join_room(match_id)
            uid_match[uid] = match_id
            match_players[match_id].add(uid)


def leave_match():
    uid = current_user.id
    with match_lock:
        try:
            match_id = uid_match[uid]  # leave match if in one
        except KeyError:
            pass
        else:
            del uid_match[uid]
            leave_room(match_id)
            match_players[match_id].remove(uid)
            if match_players[match_id].is_empty():
                del match_players[match_id]


def all_matches():
    return match_players.keys()


def all_waiting_matches():
    return [k for k, v in match_players.items() if not v.is_full()]
