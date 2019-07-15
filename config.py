# http://flask.pocoo.org/docs/1.0/config/

# Use this code to create a Mariadb database:
# CREATE DATABASE hackathon CHARACTER SET utf8 COLLATE utf8_general_ci;
# GRANT ALL ON hackathon.* TO 'hackathonuser'@'%' IDENTIFIED BY 'hackathon123' WITH GRANT OPTION;
# GRANT ALL ON hackathon.* TO 'hackathonuser'@'10.0.2.2' IDENTIFIED BY 'hackathon123' WITH GRANT OPTION;
# GRANT ALL ON hackathon.* TO 'hackathonuser'@'localhost' IDENTIFIED BY 'hackathon123' WITH GRANT OPTION;
# select host, user as username, password from mysql.user order by user; -- All Users
# UPDATE mysql.user SET Password=PASSWORD('hackathon123') WHERE User='hackathonuser'; -- Set password


import os

DEBUG = True
SECRET_KEY = '7a1bf41892db7d66f2cefc3b56955bbfec1d4ed4eefe9b53b71ab1af360d56c7'
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'hackathon.db')
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://hackathonuser:hackathon123@localhost/hackathon'
SQLALCHEMY_TRACK_MODIFICATIONS = False
ENABLE_KERBEROS = False
PARTICIPANT_SUPPORT_EMAIL = 'martious@gmail.com'
COMPANY_NAME = 'Martious'

# print(SQLALCHEMY_DATABASE_URI)
