# -*- coding: utf-8 -*-
# !/usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for
from forms import CodeForm, ResultForm, LoginForm, SignupForm
from exec_untrusted import exec_untrusted

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user
import os

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from models import User

# Configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)

# This flask-login callback is used to reload the user object from the user ID stored in the session.
# It should take the unicode ID of a user, and return the corresponding user object.
# It should return None (not raise an exception) if the ID is not valid.
@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

@app.route('/', methods=['GET', 'POST'])
@login_required
def homepage():
    code_form = CodeForm(request.form)
    result_form = ResultForm(request.form)
    
    app.logger.info(request.method)
    # app.logger.info(app.config['SQLALCHEMY_DATABASE_URI'])

    if request.method == 'POST' and code_form.validate() and code_form.code_submit.data:
        code_str = code_form.code_text.data
        result_text = exec_untrusted(code_str)
        result_form.result_text.data = result_text

    return render_template('index.html', code_form=code_form, result_form=result_form)



@app.route('/crash/')
def main():
    raise Exception()

@app.route('/testlogin/')
@login_required
def testlogin():
    return render_template('testlogin.html')

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/signup/", methods=["GET", "POST"])
def signup():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        app.logger.info('Signup Attempt, Username = ' + form.username.data + ' Name = ' + form.name.data)
        user = User(email = form.email.data,
                    username = form.username.data,
                    password = form.password.data,
                    name = form.name.data)
        db.session.add(user)
        db.session.commit()
        # flash('Welcome, {}! Please login.'.format(user.username))
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        # app.logger.info('Login Attempt, Username = ' + login_form.username.data + ' Password = ' + login_form.password.data)
        user = User.get_by_username(login_form.username.data)
        # app.logger.info(user)
        if user is not None and user.check_password(login_form.password.data):
            login_user(user, login_form.remember_me.data)
            return redirect(request.args.get('next') or url_for('testlogin'))
    return render_template('login.html',login_form=login_form)

if __name__ == "__main__":
    app.secret_key = app.config['SECRET_KEY']
    app.run(debug=app.config['DEBUG'])
