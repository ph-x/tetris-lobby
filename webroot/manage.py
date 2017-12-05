import os
from app import create_app, socketio, db

from flask_script import Manager

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    socketio.run(app, debug=True)
