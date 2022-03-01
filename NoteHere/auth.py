from flask import Blueprint, render_template as rt, url_for, flash, request, redirect
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Log In successful.', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password. Try again', category='error')
        else:
            flash('Email does not exist.', category='error')

    return rt('login.html', title='Log In', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        email1 = User.query.filter_by(email=email).first()
        username1 = User.query.filter_by(username=username).first()

        if email1:
            flash('Email already exist.', category='error')
        elif username1:
            flash('Username already taken.', category='error')
        elif len(firstName) < 1:
            flash('First Name must be greater than 1 character.', category='error')
        elif len(lastName) < 1:
            flash('Last Name must be greater than 1 character.', category='error')
        elif len(email) < 5:
            flash('Email must be greater than 5 characters.', category='error')
        elif len(username) <= 6:
            flash('Username must be at least 6 characters.', category='error')
        elif len(password1) <= 6:
            flash('Password must be at least 6 characters.', category='error')
        elif password1 != password2:
            flash('Confirm Password does not match.', category='error')
        else:
            newuser = User(firstName=firstName, lastName=lastName, email=email, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(newuser)
            db.session.commit()
            flash('Sign Up successful', category='success')
            login_user(newuser, remember=True)
            return redirect(url_for('views.home'))

    return rt('signup.html', title='Sign Up', user=current_user)
