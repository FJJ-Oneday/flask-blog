from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import login_user, logout_user, current_user, login_required
from ..forms import LoginForm, RegisterForm
from ..models import User
from ..extensions import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(name=username).first()
        if user:
            if user.check_password(password.strip()):
                login_user(user, remember=True)
                return redirect(request.referrer)
            flash('用户名或密码不正确.')
        else:
            flash('用户不存在.')
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(name=username).first()
        if user:
            flash('用户名已存在')
        else:
            user = User(name=username, email=email)
            user.password = password.strip()
            db.session.add(user)
            db.session.commit()
            flash('注册成功, 请重新登录.')
    return render_template('auth/register.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('blog.index'))