# http://flask.pocoo.org/docs/1.0/config/

import os

DEBUG = True
SECRET_KEY = '7a1bf41892db7d66f2cefc3b56955bbfec1d4ed4eefe9b53b71ab1af360d56c7'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'hackathon.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
ENABLE_KERBEROS = False

# print(SQLALCHEMY_DATABASE_URI)