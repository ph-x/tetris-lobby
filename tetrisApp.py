from flask import Flask, send_from_directory
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from flask-login import current_user
from tetrisLogic import tetris_logic
import eventlet
import redis
eventlet.monkey_patch()

app = Flask(__name__)

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)

socketio = SocketIO(app, message_queue='redis://localhost:6379/0', async_mode='eventlet')

tetris_logic.Shared.socket_out = SocketIO(message_queue='redis://localhost:6379/0')
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
    current_player.opponent = None
    for player in tetris_logic.Shared.players:
        current_player.opponent = player
        player.opponent = current_player
    tetris_logic.Shared.players.append(current_player)
def start_game():
    game = {}
    for player in tetris_logic.Shared.players:
        game[player.username]=tetris_logic.Tetris(player.username)
    tetris_logic.Shared.loser = None
    tetris_logic.Shared.game = game
#unsecure, require user authentication
@socketio.on('ready')
def on_ready(data):
    for player in tetris_logic.Shared.players:
        if player.username is current_user.username:
            player.ready()
            if player.opponent not None and player.opponent.is_ready:
                start_game()
@socketio.on('operate', namespace='/game')
def operate_game(instruction):
    game = tetris_logic.Shared.game
    game[current_user.username].operate(instruction=instruction)
if __name__ == '__main__':
    socketio.run(app, debug=True)
