from flask import Flask, send_from_directory
from flask_socketio import SocketIO
from tetrisLogic import tetris_logic


app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


# TODO: combine username and roomID
@socketio.on('start', namespace='/game')
def start_game():
    newgame = tetris_logic.Tetris()

    @socketio.on('operate', namespace='/game')
    def operate_game(instruction):
        nonlocal newgame
        newgame.operate(instruction=instruction)


if __name__ == '__main__':
    socketio.run(app)
