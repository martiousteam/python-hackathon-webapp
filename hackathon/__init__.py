# -*- coding: utf-8 -*-
# !/usr/bin/env python

from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager, current_user

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

# Initialize login_manager
# Configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "authorization.login"
login_manager.init_app(app)


@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('codesubmission.participanthome'))
    else:
        return render_template('index.html')


# -- Import a module / component using its blueprint handler variable (mod_auth)
from hackathon.mod_authorization.controllers import mod_authorization as authorization_module
# -- Register blueprint(s)
app.register_blueprint(authorization_module)


# -- Import a module / component using its blueprint handler variable (mod_auth)
from hackathon.mod_codesubmission.controllers import mod_codesubmission as codesubmission_module
# -- Register blueprint(s)
app.register_blueprint(codesubmission_module)


# Build the database:
# This will create the database file using SQLAlchemy
# db.create_all()


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.secret_key = app.config['SECRET_KEY']
    app.run(debug=app.config['DEBUG'])
