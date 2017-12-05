from . import main
from flask import url_for, redirect


@main.route('/')
def index():
    return redirect(url_for('login.do_login'))
    # return send_from_directory('static', 'room.html')

