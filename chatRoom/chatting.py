from flask import Flask, url_for, send_from_directory
from flask_socketio import SocketIO, join_room, leave_room, send, emit

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@socketio.on('connect', namespace='/chat')
def test_connect():
    emit('chat', {'username': 'system',
                  'message': 'Connected'})


@socketio.on('join', namespace='/chat')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    message = '{} has joined room {}'.format(username, room)
    emit('chat',
         {'username': 'system',
          'message': message},
         room=room)


@socketio.on('chat', namespace='/chat')
def on_chat(data):
    username = data['username']
    message = data['message']
    room = data['room']
    emit('chat',
         {'username': username,
          'message': message},
         room=room)


if __name__ == '__main__':
    socketio.run(app)
