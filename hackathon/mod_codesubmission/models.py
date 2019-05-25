# codesubmission/models.py

from hackathon import db

from hackathon.mod_authorization.models import User
from datetime import datetime

 
class Team(db.Model):
    __tablename__='team'
    __table_args__={'extend_existing':True}

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255))
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

class TeamParticipant(db.Model):
    __tablename__='team_participant'
    __table_args__={'extend_existing':True}
 
    id=db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    teamparticipant_user=db.relationship('User') 
    team_id=db.Column(db.Integer,db.ForeignKey('team.id'))
    join_date=db.Column(db.DateTime,default=datetime.utcnow)
    teamparticipant_team=db.relationship('Team')
