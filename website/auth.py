from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", "success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again", "warning")
        else:
            flash("Email is not registered!", "warning")
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def log_out():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        user_username = User.query.filter_by(username=username).first()
        if user:
            flash("Email is already registered", category="warning")
            return redirect(url_for("auth.login"))
        elif len(email) < 4:
            flash("Email is incorrect", category="warning")
        elif len(username) < 3:
            flash("Username must be greater then 2 characters", "warning")
        elif user_username:
            flash("Username is already taken", "warning")
        elif len(password1) < 8:
            flash("Password must be at least 8 characters", "warning")
        elif not password1 == password2:
            flash("Passwords do not match", "warning")
        else:
            new_user = User(username=username, email=email, password=generate_password_hash(password1, method="scrypt"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created successfully", "success")
            return redirect(url_for("views.home"))


    return render_template("sign-up.html", user=current_user)
