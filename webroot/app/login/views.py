from flask import redirect, url_for, render_template, flash, request
from flask_login import login_user, login_required, logout_user
from app.login import login
from app.models import User
from .forms import LoginForm, RegForm
from app import db


@login.route('/', methods=['GET', 'POST'])
def do_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.get_lobby'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)


@login.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))


@login.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login')
        print('ready to redirect to login page')
        return redirect(url_for('login.do_login'))
    return render_template('register.html', form=form)
