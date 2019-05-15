from sqlalchemy import desc
from flask_login import UserMixin
from hackathonapp import db
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model, UserMixin):

    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(120), unique=False)
    password_hash = db.Column(db.String)

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

    def __repr__(self):
        return "<User '{}'>".format(self.username)

if __name__ == "__main__":

    # TBD - Change create_all to create database only if file does not exist.
    db.create_all()
    # TBD - Change code to make sure record is inserted only if it does not exist.
    user = User(id=1,username='TestUser',email='martious@gmail.com',name='Test User',password='test')
    db.session.add(user)
    user = User(id=2,username='himanshu',email='himanshu.shrotri@gmail.com',name='Himanshu Shrotri',password='test')
    db.session.add(user)
    user = User(id=3,username='pratik',email='pratikajmera@gmail.com',name='Pratik Ajmera',password='test')
    db.session.add(user)
    db.session.commit()
