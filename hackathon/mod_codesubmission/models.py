# codesubmission/models.py

# Inspiration: https://www.michaelcho.me/article/many-to-many-relationships-in-sqlalchemy-models-flask


from hackathon import db
from hackathon.mod_authorization.models import User
from datetime import datetime


class Participant(db.Model):
    __tablename__='participant'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(120), unique=False)
    team_name = db.Column(db.String(120), unique=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")

    @staticmethod
    def get_by_user(user):
        return Participant.query.filter_by(user=user).first()

    def __repr__(self):
        return "(Participant '{}')".format(self.email)
    
    competitions = db.relationship("Competition", secondary="competition_participant")
    
    problemstatements = db.relationship("ProblemStatement", secondary="participant_problemstatement")
    


class Competition(db.Model): 
    __tablename__='competition'
    __table_args__={'extend_existing':True}
    
    id=db.Column(db.Integer,primary_key=True)
    
    name=db.Column(db.String(100),unique=True)
    description=db.Column(db.String(255),unique=True)
    # type=db.Column(db.String(50))#Team,Individual,Practice,etc.
    start_date=db.Column(db.DateTime)
    end_date=db.Column(db.DateTime)
    result_date=db.Column(db.DateTime)
    
    participants = db.relationship("Participant", secondary="competition_participant")

    def __repr__(self):
        return "(Competition '{}')".format(self.name)


class CompetitionParticipant(db.Model): 
    __tablename__='competition_participant'
    __table_args__={'extend_existing':True}
    
    id=db.Column(db.Integer,primary_key=True)

    participant_id=db.Column(db.Integer, db.ForeignKey('participant.id'))
    competition_id=db.Column(db.Integer, db.ForeignKey('competition.id'))

    participant=db.relationship(Participant,backref=db.backref("competition_participant", cascade="all, delete-orphan"))
    competition=db.relationship(Competition,backref=db.backref("competition_participant", cascade="all, delete-orphan"))

    def __repr__(self):
        return "(competition_id, participant_id '{},{}')".format(self.competition_id,self.participant_id)


class ProblemStatement(db.Model):
    __tablename__ = 'problemstatement'
    __table_args__={'extend_existing':True}
    
    id = db.Column(db.Integer, primary_key=True)
    problem_summary = db.Column(db.String(255))
    problem_text = db.Column(db.String(4000))
    problem_answer = db.Column(db.String(4000))
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))
    competition = db.relationship("Competition")

    participants = db.relationship("Participant", secondary="participant_problemstatement")

    def __repr__(self):
        return "(Problem Statement: '{}')".format(self.problem_text)


class ParticipantProblemStatement(db.Model): 
    __tablename__='participant_problemstatement'
    __table_args__={'extend_existing':True}
    
    id=db.Column(db.Integer,primary_key=True)

    participant_id=db.Column(db.Integer, db.ForeignKey('participant.id'))
    problemstatement_id=db.Column(db.Integer, db.ForeignKey('problemstatement.id'))

    participant=db.relationship(Participant,backref=db.backref("participant_problemstatement", cascade="all, delete-orphan"))
    problemstatement=db.relationship(ProblemStatement,backref=db.backref("participant_problemstatement", cascade="all, delete-orphan"))

    def __repr__(self):
        return "(participant_id, problemstatement_id '{},{}')".format(self.competition_id,self.problemstatement_id)


class CodeSubmission(db.Model):
    __tablename__ = 'codesubmission'
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer,db.ForeignKey('participant.id'))
    problemstatement_id = db.Column(db.Integer, db.ForeignKey('problemstatement.id'))
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))
    date_submitted = db.Column(db.DateTime,default=datetime.utcnow)
    
    code_text = db.Column(db.String(4000))
    result_text = db.Column(db.String(4000))
    is_correct = db.Column(db.Boolean)
    
    def __repr__(self):
        return "(CodeSubmission ID '{}')".format(self.id)

