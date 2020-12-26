from flask import request, render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse

from zeus import db
from zeus.auth import bp
from zeus.auth.forms import LoginForm, RegistrationForm
from zeus.database.user import User


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('automation.automation'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('auth.login'))
        login_user(user, remember=True)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('automation.automation')
        return redirect(next_page)
    return render_template('auth/login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('automation.automation'))

    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
