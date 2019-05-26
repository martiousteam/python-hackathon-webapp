# codesubmission/models.py

from hackathon import db
from hackathon.mod_authorization.models import User
from datetime import datetime


competition_participants = db.Table('competition_participants',
    db.Column('competition_id', db.Integer, db.ForeignKey('competition.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)


class Participant(User):
    participant_competitions = db.relationship('Competition',
                                               secondary=competition_participants,
                                               backref=db.backref('participants', lazy='dynamic')
                                               )
    def __repr__(self):
        return "<Participant '{}'>".format(self.name)


class Competition(db.Model): 
    __tablename__='competition'
    __table_args__={'extend_existing':True}
    # __abstract__=True
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),unique=True)
    description=db.Column(db.String(255),unique=True)
    # type=db.Column(db.String(50))#Team,Individual,Practice,etc.
    start_date=db.Column(db.DateTime)
    end_date=db.Column(db.DateTime)
    result_date=db.Column(db.DateTime)
    competition_participants = db.relationship('User',
                                               secondary=competition_participants,
                                               backref=db.backref('competitions', lazy='dynamic')
                                               )

    def __repr__(self):
        return "<Competition '{}'>".format(self.name)


class ProblemStatement(db.Model):
    __tablename__ = 'problem_statement'
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))
    problem_summary = db.Column(db.String(255))
    problem_text = db.Column(db.String)
    def __repr__(self):
        return "<Problem Statement: '{}'>".format(self.problem_txt)


class CodeSubmission(db.Model):
    __tablename__ = 'code_submissions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))
    problem_statement_id = db.Column(db.Integer, db.ForeignKey('problem_statement.id'))
    date_submitted = db.Column(db.DateTime)
    code_text = db.Column(db.String)
    result_text = db.Column(db.String)

    def __repr__(self):
        return "<CodeSubmission ID '{}'>".format(self.id)


    '''
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
    '''
