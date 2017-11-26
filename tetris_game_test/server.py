from flask import Flask, url_for, send_from_directory
from flask_socketio import SocketIO, join_room, leave_room, send, emit
import numpy as np

app = Flask(__name__)
socketio = SocketIO(app)

bitmap = [[0 for i in range(10)] for i in range(22)]

cr = 0
cc = 0

@app.route('/')
def index():
    return send_from_directory('static', 'game.html')


@socketio.on('control')
def test_connect(data):

    next = [
    [0, 1, 0],
    [1, 1, 1],
    ]

    global cr, cc, bitmap
    if data == 'left':
        cc = cc - 1
        if cc < 0:
            cc = cc + 10
    elif data == 'right':
        cc = cc + 1
        if cc > 21:
            cc = cc - 10
    elif data == 'up':
        cr = cr - 1
        if cr < 0:
            cr = cr + 22
    elif data == 'down':
        cr = cr + 1
        if cr > 9:
            cr = cr - 22
    bitmap[cr][cc] = 1
    # ATTENTION! In the response, all the strings should be included by DOUBLE QUOTATIONS, not single quotations!
    res = '{"game_bitmap": ' + str(bitmap) + ', "next": ' + str(next) + '}';
    print "current: (" + str(cr) + ", " + str(cc) + ")"
    emit('update', res)


if __name__ == '__main__':
    socketio.run(app)
