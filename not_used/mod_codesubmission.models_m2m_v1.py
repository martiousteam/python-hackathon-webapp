# codesubmission/models.py


# This implementation of many to many relationship is based on https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#association-object
# Following code can be used to insert data into this models
# 
# 
# user1 = User(id=1, username='TestUser', email='martious@gmail.com', name='Test User', password='test',
#              is_kerberos=False)
# user2 = User(id=2, username='himanshu', email='himanshu.shrotri@gmail.com', name='Himanshu Shrotri', password='test',
#              is_kerberos=False)
# user3 = User(id=3, username='pratik', email='pratikajmera@gmail.com', name='Pratik Ajmera', password='test',
#              is_kerberos=False)
# user4 = User(id=4, username='ajmera@INTRANET.MARTIOUS.COM', email='pratik.ajmera@martious.com', name='Pratik Ajmera',
#              is_kerberos=True)
# db.session.add_all([user1, user2, user3, user4])
# 
# participant1 = Participant(id=1, email='martious@gmail.com', name='Test User', user=user1)
# participant2 = Participant(id=2, email='himanshu.shrotri@gmail.com', name='Himanshu Shrotri', user=user2)
# participant3 = Participant(id=3, email='pratikajmera@gmail.com', name='Pratik Ajmera', user=user3)
# participant4 = Participant(id=4, email='pratik.ajmera@martious.com', name='Pratik Ajmera', user=user4)
# db.session.add_all([participant1, participant2, participant3, participant4])
# 
# competition1 = Competition(id=1, name='Martious Hackathon 1',
#                            description="Join in the world's most excieting Coding Competition @ Martious.com 1")
# competition2 = Competition(id=2, name='Martious Hackathon 2',
#                            description="Join in the world's most excieting Coding Competition @ Martious.com 2")
# 
# competition_participant1 = CompetitionParticipant()
# competition_participant1.participant = participant1
# competition1.participants.append(competition_participant1)
# 
# competition_participant1 = CompetitionParticipant()
# competition_participant1.participant = participant2
# competition1.participants.append(competition_participant1)
# 
# competition_participant1 = CompetitionParticipant()
# competition_participant1.participant = participant3
# competition1.participants.append(competition_participant1)
# 
# competition_participant1 = CompetitionParticipant()
# competition_participant1.participant = participant4
# competition1.participants.append(competition_participant1)
# 
# competition_participant1 = CompetitionParticipant()
# competition_participant1.participant = participant4
# competition2.participants.append(competition_participant1)
# 
# db.session.add_all([competition1, competition2])
#
#
# To extract data from this model use following patterns
# 
# participant = Participant.get_by_user(current_user)
# competitions = participant.competitions
#


from hackathon import db
from hackathon.mod_authorization.models import User
from datetime import datetime


# class Parent(Base):
#     __tablename__ = 'left'
#     id = Column(Integer, primary_key=True)
#     children = relationship("Association", back_populates="parent")


class Participant(db.Model):
    __tablename__='participant'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(120), unique=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")

    @staticmethod
    def get_by_user(user):
        return Participant.query.filter_by(user=user).first()

    def __repr__(self):
        return "(Participant '{}')".format(self.email)
    
    competitions = db.relationship("CompetitionParticipant", back_populates="participant")
    

# class Child(Base):
#     __tablename__ = 'right'
#     id = Column(Integer, primary_key=True)
#     parents = relationship("Association", back_populates="child")


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
    
    participants = db.relationship('CompetitionParticipant', back_populates='competition')

    def __repr__(self):
        return "(Competition '{}')".format(self.name)


# class Association(Base):
#    __tablename__ = 'association'
#    left_id = Column(Integer, ForeignKey('left.id'), primary_key=True)
#    right_id = Column(Integer, ForeignKey('right.id'), primary_key=True)
#    extra_data = Column(String(50))
#    child = relationship("Child", back_populates="parents")
#    parent = relationship("Parent", back_populates="children")


class CompetitionParticipant(db.Model): 
    __tablename__='competition_participant'
    __table_args__={'extend_existing':True}
    
    id=db.Column(db.Integer,primary_key=True)
    participant_id=db.Column(db.Integer, db.ForeignKey('participant.id'))
    competition_id=db.Column(db.Integer, db.ForeignKey('competition.id'))
    
    competition=db.relationship("Competition",back_populates="participants")
    participant=db.relationship("Participant",back_populates="competitions")

    def __repr__(self):
        return "(competition_id, participant_id '{},{}')".format(self.competition_id,self.participant_id)


class ProblemStatement(db.Model):
    __tablename__ = 'problemstatement'
    id = db.Column(db.Integer, primary_key=True)
    # competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))
    problem_summary = db.Column(db.String(255))
    problem_text = db.Column(db.String)
    def __repr__(self):
        return "<Problem Statement: '{}'>".format(self.problem_txt)


class CodeSubmission(db.Model):
    __tablename__ = 'codesubmission'
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    # competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))
    # problem_statement_id = db.Column(db.Integer, db.ForeignKey('problem_statement.id'))
    date_submitted = db.Column(db.DateTime)
    code_text = db.Column(db.String)
    result_text = db.Column(db.String)

    def __repr__(self):
        return "<CodeSubmission ID '{}'>".format(self.id)


    '''

competition_participants = db.Table('competition_participants',
    db.Column('competition_id', db.Integer, db.ForeignKey('competition.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)


class Participant(User):
    id=db.Column(db.Integer, primary_key=True)
    participant_competitions = db.relationship('Competition',
                                               secondary=competition_participants,
                                               backref=db.backref('participants', lazy='dynamic')
                                               )
    def __repr__(self):
        return "<Participant '{}'>".format(self.name)
    
    participant_problemstatements = db.relationship('ProblemStatement',secondary='participant_problemstatements')


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
    problemstatement_participants = db.relationship('Participant',secondary='participant_problemstatements')


class ParticipantProblemstatements(db.Model):
    __tablename__ = 'participant_problemstatements'
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    problem_statement_id = db.Column(db.Integer, db.ForeignKey('problem_statement.id'))

    participant = relationship(ProblemStatement, backref=backref("participant_problemstatements", cascade="all, delete-orphan"))
    problem_statement = relationship(Participant, backref=backref("participant_problemstatements", cascade="all, delete-orphan"))


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
