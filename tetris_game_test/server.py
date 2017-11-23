from flask import Flask, url_for, send_from_directory
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from json import dumps
import numpy as np

app = Flask(__name__)
socketio = SocketIO(app)

bitmap = [[0 for i in range(10)] for i in range(22)]
next = [[0 for i in range(4)] for i in range(4)]
next_next = next = [[0 for i in range(4)] for i in range(4)]

cr = 0
cc = 0

@app.route('/')
def index():
    return send_from_directory('static', 'game.html')


@socketio.on('control')
def test_connect(data):
    print data
    if data == 'left':
        cc = cc - 1
        if cc < 0:
            cc = cc + 22
    elif data == 'right':
        cc = cc + 1
        if cc > 21:
            cc = cc - 22
    elif data == 'up':
        cr = cr - 1
        if cr < 0:
            cr = cr + 10
    elif data == 'down':
        cr = cr + 1
        if cr > 9:
            cr = cr - 10
    bitmap[cr][cc] = 1
    next = np.random.randint(0, 1, size = [4, 4]) 
    next_next = np.random.randint(0, 1, size = [4, 4]) 
    res = "{'game_bitmap': " + dumps(bitmap) + ", 'next': " + dumps(next) + ", 'next_next': " + dumps(next_next) + "}";
    emit('update', res)


if __name__ == '__main__':
    socketio.run(app)
