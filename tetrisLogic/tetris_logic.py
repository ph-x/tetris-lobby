import copy
from flask_socketio import SocketIO, emit
from random import randint
import numpy as np
from threading import Timer
from collections import deque
from queue import Queue
from tetrisLogic.tetris_config import *
import threading
import time

class Shared:
    socket_out = None
    loser = None
    players = []

class Player:
    def __init__(self, username):
        self.username = username
        self.is_ready = False
    def ready(self):
        self.is_ready = not self.is_ready

class Canvas:
    def __init__(self):
        self.board = np.matrix([[0 for i in range(width)] for j in range(height)])
        self.board[-1] = -1                             # boundary relevant
        self.board[:, -1] = self.board[:, 0] = -1       # boundary relevant
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
        newline[:, 0] = newline[:, -1] = -1              # boundary relevant
        for line in range(height-1):                     # boundary relevant
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
            return True
        self.lastaction = 'empty'

#need opponent information
class Tetris:
    def __init__(self, username):
        self.crrt = Block()
        self.canvas = Canvas()
        self.dq = deque()
        self.username = username
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
        else:
            return picture

    def self_drop(self):
        if self.isStop:
            return
        self.dq.appendleft('down')
        t = Timer(2, self.self_drop)
        t.start()

    def stop_game(self):
        self.isStop = True
        shared.loser = self.username
        print('end')
    def operate(self, instruction):
        if self.isStop is False:
            self.dq.append(instruction)

    def run(self):
        self.draw()
        while self.isStop is False and shared.loser is None:
            if len(self.dq):
                instruction = self.dq.popleft()
                self.crrt.operate(instruction)
                picture = self.draw()
                if picture is not None:
                    shared.socket_out.emit('game', {'username':self.username, 'bitmap':str(picture.tolist())}, namespace='/game')
            else:
                time.sleep(0.01)


if __name__ == '__main__':
    tetris = Tetris()
    tetris.run()