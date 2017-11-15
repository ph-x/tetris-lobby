from tetris_config import *
import numpy as np
from random import randint
import copy
import time
import pygame


def draw_picture(picture):
    print(picture)


def get_instruction():
    return input('enter: ')


class Canvas:
    def __init__(self):
        self.board = np.matrix([[0 for i in range(width)] for j in range(height)])
        self.board[-1] = -1
        self.board[:, -1] = -1
        self.board[:, 0] = -1

    def draw(self, block):
        row = len(block.tile)
        col = len(block.tile[0])
        x = block.xoffset
        y = block.yoffset
        try:
            if np.count_nonzero(self.board[x:x + row, y:y + col] & block.tile) == 0:
                picture = copy.deepcopy(self.board)
                picture[x:x + row, y:y + col] += block.tile
                draw_picture(picture)
                return True
            else:
                return False
        except (IndexError, ValueError):
            return False

    def update(self, block):
        row = len(block.tile)
        col = len(block.tile[0])
        x = block.xoffset
        y = block.yoffset
        self.board[x:x + row, y:y + col] += block.tile
        newline = np.matrix([0 for i in range(width)])
        newline[:, 0] = newline[:, -1] = -1
        while np.count_nonzero(self.board[-2]) == width:
            self.board = np.delete(self.board, -2, 0)
            self.board = np.insert(self.board, 0, newline, 0)
            # TODO count core here


class Block:
    def __init__(self):
        self.tile = tilib[randint(0, 6)]
        # self.tile = tilib[3]
        self.xoffset = 0
        self.yoffset = width // 3
        self.lastaction = 'empty'

    def rotate(self):
        self.tile = np.rot90(self.tile)
        self.lastaction = 'rotate'

    def right_shift(self):
        self.yoffset += 1
        self.lastaction = 'rshift'

    def left_shift(self):
        self.yoffset -= 1
        self.lastaction = 'lshift'

    def drop(self):
        self.xoffset += 1
        self.lastaction = 'drop'

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


class Tetris:
    def __init__(self):
        self.crrt = Block()
        self.canvas = Canvas()
        pygame.init()
        pygame.time.set_timer(pygame.USEREVENT + 1, 2000)

    def run(self):
        operation = {
            'UP': self.crrt.rotate,
            'LEFT': self.crrt.left_shift,
            'RIGHT': self.crrt.right_shift,
            'DOWN': self.crrt.drop,
        }
        while True:
            if self.canvas.draw(self.crrt) is False:
                signal = self.crrt.recover()
                if signal is True:
                    self.canvas.update(self.crrt)
                    self.crrt = Block()
                    continue
                elif signal is False:
                    break

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.crrt.drop()
                elif event.type == pygame.QUIT:
                    break
                elif event.type == pygame.KEYDOWN:
                    for key in operation:
                        if event.key == eval("pygame.K_" + key):
                            operation[key]()

            time.sleep(2)
            # instruction = get_instruction()
            # if instruction == 'q':
            #     break
            # operation = {
            #     'UP': self.crrt.rotate,
            #     'LEFT': self.crrt.left_shift,
            #     'RIGHT': self.crrt.right_shift,
            #     'DOWN': self.crrt.drop,
            # }[instruction]()


if __name__ == '__main__':
    tetris = Tetris()
    tetris.run()