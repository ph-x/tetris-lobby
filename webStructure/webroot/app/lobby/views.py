from flask import render_template, redirect, url_for
from flask_login import current_user
from . import lobby


@lobby.route('/')
def index():
	if current_user.is_authenticated() is False:
		return redirect(url_for('auth.login'))
	else:
		return render_template('lobby/lobby.html')
