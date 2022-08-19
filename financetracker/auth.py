from flask import Blueprint, render_template, request, flash, redirect, url_for
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
        remember = request.form.get('remember')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password,password):
                flash("Logged in successfuly!",category='success')
                login_user(user,remember=True)

                if remember:
                    login_user(user,remember=True)
                else:
                    login_user(user,remember=False)

                return redirect(url_for('views.home'))
            else:
                flash("Invalid password.", category='error')
        else:
            flash("Invalid email", category='error')

    return render_template('login.html',user=current_user)


@auth.route('/logout')

def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])

def sign_up():

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exist',category='error')
        elif len(email) < 2:
            flash("Email must be more than 2 characters",category='error')
        elif len(first_name) < 2:
            flash("Name must be more than 2 characters",category='error')
        elif password1 != password2:
            flash("Password dont match",category='error')
        elif len(password1) < 7:
            flash("Password must be more than 7 characters",category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            flash("Account created",category='success')
            return redirect(url_for('views.home',user=current_user))




    return render_template('sign-up.html',user=current_user)
