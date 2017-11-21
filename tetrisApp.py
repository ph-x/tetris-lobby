from flask import Flask, url_for, send_from_directory
from flask_socketio import SocketIO, join_room, leave_room, send, emit
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
    newgame.draw()

    @socketio.on('operate', namespace='/game')
    def run_game(instruction):
        nonlocal newgame
        try:
            if newgame is not None:
                newgame.run(instruction=instruction)
        except ValueError:
            emit('gameover', "game over")
            newgame = None

if __name__ == '__main__':
    socketio.run(app)
