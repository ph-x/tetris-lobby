from flask import send_from_directory, redirect, url_for, render_template, flash
from flask_login import login_user
from webroot.app.main import main
from webroot.app.models import User
from .forms import LoginForm


@main.route('/login', methods=['GET'])
def get_login():
    return send_from_directory('static', 'login.html')


@main.route('/login', methods=['POST'])
def do_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.get_lobby'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)
