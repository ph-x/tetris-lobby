import threading
from flask_socketio import join_room, leave_room

match_lock = threading.Lock()  # guards the following 2 data structures
sid_match = {}
match_nplayers = {}

reserved_rooms = {'lobby_chat': 0}  # todo: automatic enumerate

id_lock = threading.Lock()  # guards the match id
next_match = len(reserved_rooms)


def new_match(sid):
    global next_match
    with id_lock:
        match_id = next_match
        next_match += 1
    with match_lock:  # may not be necessary
        sid_match[sid] = match_id
        match_nplayers[match_id] = 1
    return match_id


def join_match(match_id, sid):
    with match_lock:
        try:
            nplayers = match_nplayers[match_id]
        except KeyError:
            raise RuntimeError(
                'user {} wants to join nonexistent match {}'.format(sid, match_id))
        else:
            if nplayers >= 2:
                raise RuntimeError('match {} is full'.format(match_id))
            if sid in sid_match:
                raise RuntimeError('user {} already in match {}'.format(sid, sid_match[sid]))
            join_room(match_id, sid)
            sid_match[sid] = match_id


def leave_match(sid):
    with match_lock:
        match_id = sid_match[sid]
        del sid_match[sid]
        leave_room(match_id, sid)
        match_nplayers[match_id].nplayers -= 1
        if match_nplayers[match_id].nplayers == 0:
            del match_nplayers[match_id]


def all_matches():
    return match_nplayers.keys()


def all_waiting_matches():
    return [k for k, v in match_nplayers.items() if v < 2]
