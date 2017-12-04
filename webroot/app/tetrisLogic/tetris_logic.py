import copy
from random import randint
import numpy as np
from threading import Timer
from collections import deque
from .tetris_config import *
from .. import children_socket
import threading
import time
import json


# room details, destroyed when no player in room
class RoomInfo:
    def __init__(self, room_id):
        self.socket_out = children_socket
        self.loser = None
        # sid -> Player
        self.players = {}
        # sid -> Tetris
        self.game = {}
        # game status : waiting, on, end
        self.game_status = 'waiting'
        self.room_id = room_id


# player in room, destroyed when quit
class Player:
    def __init__(self, sid, username):
        self.sid = sid
        self.username = username
        self.is_ready = False

    def ready(self):
        self.is_ready = not self.is_ready


class Canvas:
    def __init__(self):
        self.board = np.matrix([[0 for i in range(width)] for j in range(height)])
        self.board[-1] = -1  # boundary relevant
        self.board[:, -1] = self.board[:, 0] = -1  # boundary relevant

    def draw(self, block):
        row = len(block.tile)
        col = len(block.tile[0])
        x = block.xoffset
        y = block.yoffset
        try:
            if np.count_nonzero(self.board[x:x + row, y:y + col] & block.tile) == 0:
                picture = copy.deepcopy(self.board)
                picture[x:x + row, y:y + col] += block.tile
                return picture
            else:
                return None
        except (IndexError, ValueError):
            return None

    def update(self, block):
        row = len(block.tile)
        col = len(block.tile[0])
        x = block.xoffset
        y = block.yoffset
        self.board[x:x + row, y:y + col] += block.tile
        newline = np.matrix([0 for i in range(width)])
        newline[:, 0] = newline[:, -1] = -1  # boundary relevant
        for line in range(height - 1):  # boundary relevant
            if np.count_nonzero(self.board[line]) == width:
                self.board = np.delete(self.board, line, 0)
                self.board = np.insert(self.board, 0, newline, 0)
                # TODO count core here


class Block:
    def __init__(self):
        self.tile = tilib[randint(0, 6)]
        self.xoffset = 0
        self.yoffset = width // 3
        self.lastaction = 'empty'

    def operate(self, instruction):
        if instruction == "left":
            self.yoffset -= 1
            self.lastaction = 'lshift'
        elif instruction == "right":
            self.yoffset += 1
            self.lastaction = 'rshift'
        elif instruction == "down":
            self.xoffset += 1
            self.lastaction = 'drop'
        elif instruction == "up":
            self.tile = np.rot90(self.tile)
            self.lastaction = 'rotate'

    def recover(self):
        if self.lastaction == 'empty':
            return False
        elif self.lastaction == 'rotate':
            self.tile = np.rot90(self.tile, -1)
        elif self.lastaction == 'rshift':
            self.yoffset -= 1
        elif self.lastaction == 'lshift':
            self.yoffset += 1
        elif self.lastaction == 'drop':
            self.xoffset -= 1
            self.lastaction = 'empty'
            return True
        self.lastaction = 'empty'


# need opponent information
class Tetris:
    def __init__(self, sid, room_info):
        self.crrt = Block()
        self.canvas = Canvas()
        self.dq = deque()
        self.sid = sid
        self.room_info = room_info
        self.isStop = False
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        self.self_drop()

    def draw(self):
        picture = self.canvas.draw(self.crrt)
        if picture is None:
            signal = self.crrt.recover()
            if signal is True:
                self.canvas.update(self.crrt)
                self.crrt = Block()
            elif signal is False:
                self.stop_game()

        return picture

    def self_drop(self):
        if self.isStop or self.room_info.loser is not None:
            return
        self.dq.appendleft('down')
        t = Timer(1, self.self_drop)
        t.start()

    def stop_game(self):
        self.isStop = True
        print('end')
        self.room_info.loser = self.sid
        self.room_info.game_status = 'end'
        for psid in self.room_info.players:
            self.room_info.players[psid].is_ready = False
            data = {'action': 'end'}
            if psid is self.sid:
                data['loser'] = 'left'
            else:
                data['loser'] = 'right'
            self.room_info.socket_out.emit('game_status', json.dumps(data), room=psid, namespace='/game')
            self.room_info.game = {}

    def operate(self, instruction):
        if self.isStop is False:
            self.dq.append(instruction)

    def run(self):
        while self.isStop is False and self.room_info.loser is None:
            if len(self.dq):
                instruction = self.dq.popleft()
                self.crrt.operate(instruction)
                picture = self.draw()
                if picture is None:
                    self.draw()
                    continue
                data = {'bitmap': (picture[0:-1, 1:-1].tolist())}
                for psid in self.room_info.players:
                    if psid is self.sid:
                        data['player'] = 'left'
                    else:
                        data['player'] = 'right'
                    self.room_info.socket_out.emit('game_msg', json.dumps(data), room=psid, namespace='/game')
            else:
                time.sleep(0.01)


if __name__ == '__main__':
    tetris = Tetris(sid='test', room_info=None)
    tetris.run()
