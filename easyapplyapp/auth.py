import functools
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from .db import db_session
from .models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        
        if error is None:
            find_user = User.query.filter(User.name == username).first()
            if find_user is None:
                try:
                    user = User(name=username, password=generate_password_hash(password))
                    db_session.add(user)
                    db_session.commit()
                    error = "Please login via the login page"
                except:
                    error = f"Unable to add user {username} to database"
            else:
                error = f"user {username} is already registered"

        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.query.filter(User.name == username).first()

        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user.password, password):
            error = "Incorrect password"
        
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        user = None
    else:
        user = User.query.filter(User.id == user_id).first()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('user_id') is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
        