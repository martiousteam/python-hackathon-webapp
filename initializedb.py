import sys
# sys.path.insert(0,"/var/www/python/python-hackathon-webapp/")

from hackathon import db
from hackathon import app
from hackathon.mod_authorization.models import User
from hackathon.mod_codesubmission.models import Participant, Competition, CompetitionParticipant, ProblemStatement, ParticipantProblemStatement


if __name__ == "__main__":
    # TBD - Change create_all to create database only if file does not exist.
    with app.test_request_context():
        db.init_app(app)
        db.create_all()

    # TBD - Change code to make sure record is inserted only if it does not exist.
    users=[]
    users.append(User(id=1,username='TestUser',email='martious@gmail.com',name='Test User',password='test',is_kerberos=False))
    users.append(User(id=2,username='himanshu',email='himanshu.shrotri@gmail.com',name='Himanshu Shrotri',password='test',is_kerberos=False))
    users.append(User(id=3,username='pratik',email='pratikajmera@gmail.com',name='Pratik Ajmera',password='test',is_kerberos=False))
    users.append(User(id=4,username='ajmera@INTRANET.MARTIOUS.COM',email='pratik.ajmera@martious.com',name='Pratik Ajmera',is_kerberos=True))
    db.session.add_all(users)

    participants=[]
    participants.append(Participant(id=1,email='martious@gmail.com',name='Test User',user_id=1,team_name='Martious 1'))
    participants.append(Participant(id=2,email='himanshu.shrotri@gmail.com',name='Himanshu Shrotri',user_id=2,team_name='Martious 2'))
    participants.append(Participant(id=3,email='pratikajmera@gmail.com',name='Pratik Ajmera',user_id=3,team_name='Martious 1'))
    participants.append(Participant(id=4,email='pratik.ajmera@martious.com',name='Pratik Ajmera',user_id=4,team_name='Martious 2'))
    db.session.add_all(participants)

    competitions=[]
    competitions.append(Competition(id=1,name='Hackathon 1', description="Join in the world's most excieting Coding Competition @ Martious.com 1"))
    competitions.append(Competition(id=2,name='Hackathon 2', description="Join in the world's most excieting Coding Competition @ Martious.com 2"))

    # First pattern to insert data in relationship
    competitions[0].participants.append(participants[0])
    competitions[0].participants.append(participants[1])
    
    db.session.add_all(competitions)
    
    # Another pattern to insert data in relationship
    competitionparticipants=[]
    competitionparticipants.append(CompetitionParticipant(participant_id=3,competition_id=1))
    competitionparticipants.append(CompetitionParticipant(participant_id=4,competition_id=1))
    competitionparticipants.append(CompetitionParticipant(participant_id=1,competition_id=2))

    db.session.add_all(competitionparticipants)

    problemstatements=[]
        
    problemstatements.append(ProblemStatement(competition_id=1, problem_summary="Problem Summary 1.1",
                                         problem_text="Sample Problem Text Goes Here 1", problem_answer="hello"))
                                         
    problemstatements.append(ProblemStatement(competition_id=1, problem_summary="Problem Summary 1.2",
                                         problem_text="Sample Problem Text Goes Here 2", problem_answer="100"))

    problemstatements.append(ProblemStatement(competition_id=2, problem_summary="Problem Summary 2.1",
                                         problem_text="Sample Problem Text Goes Here 3", problem_answer="hello"))

    problemstatements.append(ProblemStatement(competition_id=2, problem_summary="Problem Summary 2.2",
                                         problem_text="Sample Problem Text Goes Here 4", problem_answer="1220"))

    problemstatements.append(ProblemStatement(competition_id=2, problem_summary="Problem Summary 2.3",
                                         problem_text="Sample Problem Text Goes Here 5", problem_answer="123"))

    problemstatements.append(ProblemStatement(competition_id=2, problem_summary="Problem Summary 2.4",
                                         problem_text="Sample Problem Text Goes Here 6", problem_answer="115"))

    db.session.add_all(problemstatements)
    
    participantproblemstatements=[]

    participantproblemstatements.append(ParticipantProblemStatement(participant_id=1,problemstatement_id=1))
    participantproblemstatements.append(ParticipantProblemStatement(participant_id=2,problemstatement_id=2))
    participantproblemstatements.append(ParticipantProblemStatement(participant_id=3,problemstatement_id=3))
    participantproblemstatements.append(ParticipantProblemStatement(participant_id=4,problemstatement_id=1))

    db.session.add_all(participantproblemstatements)

    db.session.commit()
