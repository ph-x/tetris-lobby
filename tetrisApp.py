from flask import Flask, send_from_directory
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room, \
    close_room, rooms, disconnect
#from flask-login import current_user
from tetrisLogic import tetris_logic
import eventlet
import redis
eventlet.monkey_patch()

app = Flask(__name__)

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)

socketio = SocketIO(app, message_queue='redis://localhost:6379/0', async_mode='eventlet')

tetris_logic.shared.socket_out = SocketIO(message_queue='redis://localhost:6379/0')
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')
#unsecure, require user authentication
@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    current_player=tetris_logic.Player(username)
    for player in tetris_logic.shared.players:
        current_player.opponent = player
        player.opponent = current_player
    tetris_logic.shared.players.append(current_player)
#unsecure, require user authentication
@socketio.on('ready')
def on_ready(data):
    for player in tetris_logic.shared.players:
        if player.username is data['username']:
            player.ready()
# TODO: combine username and roomID
@socketio.on('start', namespace='/game')
def start_game():
    tetris_logic.shared.winner = None
    game = [None, None]
    game[0] = tetris_logic.Tetris(0)
    game[1] = tetris_logic.Tetris(1)
    @socketio.on('operate', namespace='/game')
    def operate_game(instruction):
        nonlocal game
        game[0].operate(instruction=instruction)
        game[1].operate(instruction=instruction)
if __name__ == '__main__':
    socketio.run(app, debug=True)
