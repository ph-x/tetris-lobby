from . import main
from flask import url_for, redirect
from flask_login import current_user


@main.route('/')
def index():
    if current_user.is_authenticated() is False:
        return redirect(url_for('login.do_login'))
    else:
        return redirect(url_for('main.get_lobby'))
    # return send_from_directory('static', 'room.html')

