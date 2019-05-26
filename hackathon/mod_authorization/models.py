# mod_authorization/models.py

from flask_login import UserMixin
from hackathon import db
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model, UserMixin):
    __tablename__='user'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(120), unique=False)
    password_hash = db.Column(db.String)
    is_kerberos = db.Column(db.Boolean, default=False)


    # this creates a property for this class which is not stored in database
    # this property can not be read
    @property
    def password(self):
        raise AttributeError('password: write-only field')

    # Setter method for password property
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_by_kerberosuser(username):
        return User.query.filter_by(username=username).filter_by(is_kerberos=True).first()

    def __repr__(self):
        return "<User '{}'>".format(self.username)
