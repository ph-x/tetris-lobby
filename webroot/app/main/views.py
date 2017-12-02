from . import main
from flask import send_from_directory


@main.route('/')
def index():
    return send_from_directory('static', 'room.html')

